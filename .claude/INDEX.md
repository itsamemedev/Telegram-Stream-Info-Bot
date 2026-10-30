# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
 10001  GET              /                                                dashboard
 12048  GET              /api/abo/status                                  api_abo_status
 12002  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 10789  GET              /api/automation/status                           api_automation_status
 10811  POST             /api/automation/toggle                           api_automation_toggle
 19507  GET              /api/channel/categories                          api_channel_categories
 19513  POST             /api/channel/set                                 api_channel_set
 19360  GET              /api/channels/status                             api_channels_status
 19034  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 19017  GET              /api/clips                                       api_clips
 19063  POST/DELETE      /api/clips/clear                                 api_clips_clear
 18935  GET              /api/debug/threads                               api_debug_threads
 12013  GET              /api/events                                      api_events
 11497  GET              /api/events/stream                               api_events_stream
 11324  GET              /api/health                                      api_health
 18976  POST             /api/highlights/config                           api_highlights_config
  9935  POST             /api/login                                       dashboard_login_submit
 12338  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 11412  GET              /api/notify/status                               api_notify_status
 11423  POST             /api/notify/test                                 api_notify_test
 12102  GET              /api/proxy/heatmap                               api_proxy_heatmap
 12079  GET              /api/proxy/trend                                 api_proxy_trend
 19083  GET              /api/tts/<fn>                                    api_tts_file
 19858  GET              /api/upload_window                               api_upload_window
 11614  GET              /archive/<int:eid>/download                      archive_download
 11642  GET              /download/<int:recording_id>                     download
 11571  GET              /health                                          health
 18850  GET              /healthz                                         healthz
  9926  GET              /login                                           dashboard_login_page
  9956  GET              /logout                                          dashboard_logout
  9963  GET              /manifest.webmanifest                            pwa_manifest
 19831  GET              /overlay                                         overlay_page
  9987  GET              /pwa-icon-<variant>.png                          pwa_icon
  9973  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (338)

```
   195  GET              /api/active-recordings                           api_active_recordings   [nc/routes/auskunft.py]
   422  GET              /api/activity-pulse                              api_activity_pulse   [nc/routes/auskunft.py]
   195  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   165  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
   993  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   738  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   864  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   844  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   882  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   806  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   356  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   367  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   377  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   400  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   407  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   418  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   546  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   644  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1231  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1263  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   341  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   946  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   926  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1099  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1147  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1198  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1057  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   901  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   499  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   763  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   645  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   628  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   620  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   456  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   472  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   807  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   374  GET              /api/archive/scan                                api_archive_scan   [nc/routes/archive.py]
   405  POST             /api/archive/scan/adopt                          api_archive_scan_adopt   [nc/routes/archive.py]
   772  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   792  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   679  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    49  GET/POST         /api/audio/config                                api_audio_config   [nc/routes/audio.py]
    78  POST             /api/audio/testtone                              api_audio_testtone   [nc/routes/audio.py]
   216  GET/POST         /api/auto-archive-rules                          api_archive_rules   [nc/routes/wartung.py]
   241  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete   [nc/routes/wartung.py]
   246  POST             /api/auto-archive-rules/run                      api_archive_rules_run   [nc/routes/wartung.py]
   163  GET              /api/azrael/agents                               api_azrael_agents   [nc/routes/azrael.py]
    99  POST             /api/azrael/ask                                  api_azrael_ask   [nc/routes/azrael.py]
   222  GET/POST         /api/azrael/context                              api_azrael_context   [nc/routes/azrael.py]
   120  GET              /api/azrael/core                                 api_azrael_core   [nc/routes/azrael.py]
   342  POST             /api/azrael/live_pause                           api_azrael_live_pause   [nc/routes/azrael.py]
   328  GET              /api/azrael/live_status                          api_azrael_live_status   [nc/routes/azrael.py]
   350  POST             /api/azrael/live_test                            api_azrael_live_test   [nc/routes/azrael.py]
   174  GET              /api/azrael/memories                             api_azrael_memories   [nc/routes/azrael.py]
   406  POST             /api/azrael/persona                              api_azrael_persona_set   [nc/routes/azrael.py]
   397  GET              /api/azrael/personas                             api_azrael_personas   [nc/routes/azrael.py]
   314  GET              /api/azrael/piper_status                         api_azrael_piper_status   [nc/routes/azrael.py]
   190  POST             /api/azrael/react                                api_azrael_react   [nc/routes/azrael.py]
   231  GET              /api/azrael/reaction                             api_azrael_reaction   [nc/routes/azrael.py]
   243  GET              /api/azrael/reactions                            api_azrael_reactions   [nc/routes/azrael.py]
   372  GET              /api/azrael/transcript                           api_azrael_transcript   [nc/routes/azrael.py]
   281  POST             /api/azrael/tts_test                             api_azrael_tts_test   [nc/routes/azrael.py]
   267  GET              /api/azrael/voices                               api_azrael_voices   [nc/routes/azrael.py]
   379  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model   [nc/routes/azrael.py]
   288  GET              /api/backoff-watch                               api_backoff_watch   [nc/routes/beobachtung.py]
   208  POST             /api/backup/run                                  api_backup_run   [nc/routes/wartung.py]
   174  GET              /api/backup/status                               api_backup_status   [nc/routes/wartung.py]
   157  POST             /api/backup/system                               api_backup_system   [nc/routes/wartung.py]
   399  GET              /api/bandwidth/live                              api_bandwidth_live   [nc/routes/auskunft.py]
   376  GET              /api/bookmarks                                   api_bookmarks_list   [nc/routes/auskunft.py]
   198  GET              /api/brain                                       api_brain   [nc/routes/brain.py]
   131  GET              /api/brain/alarms                                api_brain_alarms   [nc/routes/brain.py]
   116  GET              /api/brain/creator                               api_brain_creator   [nc/routes/brain.py]
    93  GET              /api/brain/graph                                 api_brain_graph   [nc/routes/brain.py]
   158  GET              /api/brain/growth                                api_brain_growth   [nc/routes/brain.py]
    80  GET              /api/brain/health                                api_brain_health   [nc/routes/brain.py]
    81  POST             /api/chat/send                                   api_chat_send   [nc/routes/chat.py]
    53  GET              /api/chat/send_status                            api_chat_send_status   [nc/routes/chat.py]
   174  GET              /api/checks                                      api_checks   [nc/routes/auskunft.py]
    40  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    52  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    52  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    87  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   122  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   443  GET              /api/community/stats                             api_community_stats   [nc/routes/auskunft.py]
   433  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   418  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   238  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
   195  POST             /api/cookies/fetch                               api_cookies_fetch   [nc/routes/settings.py]
    73  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    80  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   497  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
   259  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   286  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   379  POST             /api/db/restore/apply                            api_db_restore_apply   [nc/routes/settings.py]
   323  GET              /api/db/restore/list                             api_db_restore_list   [nc/routes/settings.py]
   341  POST             /api/db/restore/prepare                          api_db_restore_prepare   [nc/routes/settings.py]
   246  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
   164  GET              /api/defense/attacks                             api_defense_attacks   [nc/routes/abwehr.py]
   125  GET              /api/defense/crowdsec                            api_defense_crowdsec   [nc/routes/abwehr.py]
   146  GET              /api/defense/fail2ban                            api_defense_fail2ban   [nc/routes/abwehr.py]
    91  GET              /api/defense/overview                            api_defense_overview   [nc/routes/abwehr.py]
   244  POST             /api/discord/announce                            api_discord_announce   [nc/routes/discord.py]
   170  GET              /api/discord/clips_week                          api_discord_clips_week   [nc/routes/discord.py]
   188  GET              /api/discord/community                           api_discord_community   [nc/routes/discord.py]
   160  GET              /api/discord/invite                              api_discord_invite   [nc/routes/discord.py]
    63  GET              /api/discord/overview                            api_discord_overview   [nc/routes/discord.py]
   136  POST             /api/discord/webhook_test                        api_discord_webhook_test   [nc/routes/discord.py]
    79  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
   112  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   120  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    60  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   136  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
   194  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   179  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    90  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
   112  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   133  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
   150  POST             /api/evolution/proposals/bulk                    api_evolution_bulk   [nc/routes/evolution.py]
    80  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   209  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    44  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   200  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   220  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   247  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
   394  GET              /api/forecast/storage                            api_forecast_storage   [nc/routes/auskunft.py]
   297  GET              /api/freeai/status                               api_freeai_status   [nc/routes/auskunft.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   414  GET              /api/heatmap/lives/<username>                    api_heatmap_lives   [nc/routes/auskunft.py]
   409  GET              /api/heatmap/recordings                          api_heatmap_recordings   [nc/routes/auskunft.py]
   485  GET              /api/highlights                                  api_highlights   [nc/routes/auskunft.py]
    64  GET              /api/i18n/katalog                                api_i18n_katalog   [nc/routes/i18n.py]
    53  GET              /api/i18n/sprachen                               api_i18n_sprachen   [nc/routes/i18n.py]
   307  GET              /api/i18n/uebersetzer.js                         api_i18n_js   [nc/routes/i18n.py]
    77  POST             /api/i18n/waehlen                                api_i18n_waehlen   [nc/routes/i18n.py]
   168  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    43  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   150  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   125  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   189  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    76  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    99  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   223  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   222  GET              /api/kick/channel                                api_kick_channel   [nc/routes/kick.py]
   244  POST             /api/kick/channel                                api_kick_channel_set   [nc/routes/kick.py]
   103  GET              /api/kick/oauth/callback                         api_kick_oauth_callback   [nc/routes/kick.py]
   171  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect   [nc/routes/kick.py]
   149  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect   [nc/routes/kick.py]
    85  GET              /api/kick/oauth/start                            api_kick_oauth_start   [nc/routes/kick.py]
   128  GET              /api/kick/oauth/status                           api_kick_oauth_status   [nc/routes/kick.py]
   178  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck   [nc/routes/kick.py]
   119  POST             /api/kickmod/config                              api_kickmod_config   [nc/routes/kickmod.py]
   167  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords   [nc/routes/kickmod.py]
   184  GET              /api/kickmod/learned                             api_kickmod_learned   [nc/routes/kickmod.py]
   215  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear   [nc/routes/kickmod.py]
   191  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote   [nc/routes/kickmod.py]
   251  POST             /api/kickmod/say                                 api_kickmod_say   [nc/routes/kickmod.py]
   221  POST             /api/kickmod/start                               api_kickmod_start   [nc/routes/kickmod.py]
    82  GET              /api/kickmod/status                              api_kickmod_status   [nc/routes/kickmod.py]
   235  POST             /api/kickmod/stop                                api_kickmod_stop   [nc/routes/kickmod.py]
    66  GET              /api/lagebild                                    api_lagebild   [nc/routes/lagebild.py]
   428  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard   [nc/routes/auskunft.py]
    78  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
   103  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
   113  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    52  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    70  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   225  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
   100  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    66  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    77  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   142  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   137  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   128  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    53  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    92  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
   257  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   324  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   352  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   203  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   270  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   505  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    80  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   168  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   151  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   391  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   238  GET              /api/outcomes                                    api_outcomes   [nc/routes/auskunft.py]
   210  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   193  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
    94  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   179  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   495  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   470  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   308  GET              /api/public/stats                                api_public_stats   [nc/routes/auskunft.py]
   144  GET              /api/pulse                                       api_pulse   [nc/routes/auskunft.py]
   973  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
  1082  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
  1110  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
  1130  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   960  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
  1022  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
  1009  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   990  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   347  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   635  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   630  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   678  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   561  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   888  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   652  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   615  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   588  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   862  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   732  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   821  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   727  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   660  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   440  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   905  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   528  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   783  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   938  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   923  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   484  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   722  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   708  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   691  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   748  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
  1273  GET              /api/recordings/session/<sid>                    api_recording_session   [nc/routes/recordings.py]
  1394  POST             /api/recordings/session/<sid>/join               api_recording_session_join   [nc/routes/recordings.py]
  1237  GET              /api/recordings/sessions                         api_recording_sessions   [nc/routes/recordings.py]
   841  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   737  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   490  POST             /api/restream/<int:rid>/delete                   api_restream_delete   [nc/routes/restream.py]
   468  POST             /api/restream/<int:rid>/edit                     api_restream_edit   [nc/routes/restream.py]
   509  POST             /api/restream/<int:rid>/start                    api_restream_start   [nc/routes/restream.py]
   526  POST             /api/restream/<int:rid>/stop                     api_restream_stop   [nc/routes/restream.py]
   578  GET              /api/restream/chatfeed                           api_restream_chatfeed   [nc/routes/restream.py]
   444  POST             /api/restream/create                             api_restream_create   [nc/routes/restream.py]
   265  GET              /api/restream/deck                               api_restream_deck   [nc/routes/restream.py]
   165  GET              /api/restream/health                             api_restream_health   [nc/routes/restream.py]
   600  POST             /api/restream/layout                             api_restream_layout   [nc/routes/restream.py]
   413  GET              /api/restream/list                               api_restream_list   [nc/routes/restream.py]
   134  POST             /api/restream/report                             api_restream_report   [nc/routes/restream.py]
   539  POST             /api/restream/start_all                          api_restream_start_all   [nc/routes/restream.py]
   565  POST             /api/restream/stop_all                           api_restream_stop_all   [nc/routes/restream.py]
   191  GET              /api/restream/testpush                           api_testpush_status   [nc/routes/restream.py]
   216  POST             /api/restream/testpush                           api_testpush_run   [nc/routes/restream.py]
   388  GET              /api/restream/verify                             api_restream_verify   [nc/routes/restream.py]
   134  GET              /api/retention/preview                           api_retention_preview   [nc/routes/wartung.py]
   144  POST             /api/retention/run                               api_retention_run   [nc/routes/wartung.py]
   474  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   464  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   499  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    65  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    86  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    52  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
   102  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   366  GET              /api/search                                      api_search   [nc/routes/auskunft.py]
    92  GET              /api/selftest                                    api_selftest   [nc/routes/selbsttest.py]
   456  GET              /api/shield/stats                                api_shield_stats   [nc/routes/auskunft.py]
   128  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   219  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   214  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   274  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   110  GET              /api/storage                                     api_storage   [nc/routes/wartung.py]
   116  POST             /api/storage/cleanup                             api_storage_cleanup   [nc/routes/wartung.py]
   483  GET              /api/stream/inspect/<username>                   api_stream_inspect   [nc/routes/beobachtung.py]
   342  GET              /api/stream/timeline                             api_stream_timeline   [nc/routes/beobachtung.py]
   372  GET              /api/stream/transcript                           api_stream_transcript   [nc/routes/beobachtung.py]
   126  GET              /api/streamer/compare                            api_streamer_compare   [nc/routes/streamer.py]
   273  POST             /api/streamer/delete/<username>                  api_streamer_delete   [nc/routes/streamer.py]
    88  GET              /api/streamer/detail                             api_streamer_detail   [nc/routes/streamer.py]
   298  GET              /api/streamer/digest/<username>                  api_streamer_digest   [nc/routes/streamer.py]
   230  GET              /api/streamer/dormant                            api_streamer_dormant   [nc/routes/streamer.py]
   254  GET              /api/streamer/exists/<username>                  api_streamer_exists   [nc/routes/streamer.py]
   185  GET              /api/streamer/journal/<username>                 api_streamer_journal   [nc/routes/streamer.py]
   150  GET/POST         /api/streamer/priority/<username>                api_streamer_priority   [nc/routes/streamer.py]
   210  GET              /api/streamer/watchlist                          api_streamer_watchlist   [nc/routes/streamer.py]
    56  GET              /api/streamers/wall                              api_streamers_wall   [nc/routes/streamer.py]
   219  GET              /api/summary/preview                             api_summary_preview   [nc/routes/auskunft.py]
    74  GET              /api/system                                      api_system   [nc/routes/systemlage.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   178  GET              /api/system/check_timing                         api_check_timing   [nc/routes/systemlage.py]
   118  GET              /api/system/config_drift                         api_config_drift   [nc/routes/systemlage.py]
   141  GET              /api/system/config_snapshot                      api_system_config_snapshot   [nc/routes/systemlage.py]
   238  GET              /api/system/preflight                            api_system_preflight   [nc/routes/systemlage.py]
   105  GET              /api/system/preflight_history                    api_system_preflight_history   [nc/routes/systemlage.py]
   375  GET              /api/system/resilience                           api_system_resilience   [nc/routes/systemlage.py]
   389  GET              /api/tags                                        api_tags_list   [nc/routes/auskunft.py]
   189  GET              /api/top                                         api_top   [nc/routes/auskunft.py]
   238  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   453  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   482  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   402  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   415  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   511  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   388  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   263  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   308  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   332  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   319  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   165  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   277  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   135  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   369  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   424  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   265  GET              /api/trend-7d                                    api_trend_7d   [nc/routes/auskunft.py]
   121  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
   100  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   132  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
   113  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   125  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback   [nc/routes/twitch.py]
    77  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect   [nc/routes/twitch.py]
   101  GET              /api/twitch/oauth/start                          api_twitch_oauth_start   [nc/routes/twitch.py]
    55  GET              /api/twitch/oauth/status                         api_twitch_oauth_status   [nc/routes/twitch.py]
   453  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   419  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   478  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   458  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   441  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   434  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
   251  GET              /api/userstats                                   api_userstats   [nc/routes/auskunft.py]
   317  GET              /api/version                                     api_version   [nc/routes/auskunft.py]
    52  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    92  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   123  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
   107  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
   131  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback   [nc/routes/youtube.py]
   152  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget   [nc/routes/youtube.py]
   164  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout   [nc/routes/youtube.py]
    89  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect   [nc/routes/youtube.py]
   113  GET              /api/youtube/oauth/start                         api_youtube_oauth_start   [nc/routes/youtube.py]
    67  GET              /api/youtube/oauth/status                        api_youtube_oauth_status   [nc/routes/youtube.py]
   199  GET              /api/youtube/sendrate                            api_youtube_sendrate   [nc/routes/youtube.py]
    73  GET              /fonts/<name>                                    schrift   [nc/routes/schriften.py]
    66  GET              /fonts/schriften.css                             schriften_css   [nc/routes/schriften.py]
   414  GET              /metrics                                         api_prometheus_metrics   [nc/routes/beobachtung.py]
```

## Discord-Slash-Commands in discordbot.py (65)

```
  2082  /about                  Ueber diesen Bot
   809  /ai                     
  2082  /aireset                KI-Kontext zuruecksetzen
  1213  /ask                    
   910  /assign_role            
   960  /ban                    
  2037  /botstats               
  2082  /brain                  Brain-Lage: Regeln, Agenten, Empfehlungen
  2082  /bulkadd                Mehrere User auf einmal tracken · a b c
  2082  /cleanup                Alte Aufnahmen aufraeumen
  1468  /clearwarns             
  2001  /clip                   
  1986  /clipoftheweek          
  1339  /clips                  
  2082  /cookies                Cookie-Status — mit 'holen' selbst beziehen · [holen]
   865  /create_category        
   836  /create_channel         
   900  /create_group           
   875  /create_role            
   851  /create_voice           
  1096  /daily                  
  2082  /diag                   Vollstaendige Diagnose
  2082  /einnahmen              Einnahmen und Spenden
  1242  /event                  
  1284  /events                 
  1378  /follow                 
  1367  /help                   
   950  /kick                   
  1071  /leaderboard            
  2082  /live                   Live-Status sofort pruefen · @user
  1326  /livenow                
  2082  /logs                   Letzte Fehler aus dem Log
  2082  /pause                  Tracking pausieren · @user
  1354  /post_test              
  1174  /profile                
   982  /purge                  
  2082  /quota                  Speicher-Quota
  1058  /rank                   
  1314  /recstatus              
   920  /remove_role            
  2082  /report                 Azrael-Sentinel-Wochenreport
   822  /restream_status        
  2082  /resume                 Tracking fortsetzen · @user
   930  /set_channel_perms      
  1025  /setup_community        
  1042  /setup_targets          
  1410  /stats                  
   781  /status                 
  2082  /stoprec                Laufende Aufnahme sauber beenden · @user
  1506  /streaminfo             
  2082  /summary                Tageszusammenfassung
  2082  /sysres                 System-Ressourcen
  2082  /teststream             Recorder-Selbsttest · @user
  2082  /tiktok                 Profil-Analyse eines TikTok-Accounts · ‹name›
   970  /timeout                
  1478  /topstreamers           
  2082  /topusers               Top-Streamer nach Aufnahmen
   711  /track                  
  2082  /track_exact            Exakten Usernamen tracken (ohne Korrektur) · ‹name›
   794  /tracklist              
  1392  /unfollow               
  2082  /unpause                Auto-pausierte Quelle wieder aktivieren · @user
   743  /untrack                
  1431  /warn                   
  1454  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2240  on_member_join
  2202  on_message
  2103  on_raw_reaction_add
  2275  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    58-73     konfiguriere
    76-456    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (46 Funktionen)

```
  1583-1634   _award_xp
  1805-1834   _clip_week_leader
  1858-1872   _clipoftheweek_loop
  2391-2453   _community_events_loop
  1540-1562   _dc_client
  1565-1574   _dc_offen
  2493-2528   _disc_automod_check
   401-406    _disc_sprache_setzen
  1637-1685   _discord_ai_automod
   534-573    _discord_automod
  1688-1708   _discord_azrael_reply
  1875-2350   _discord_run_once
   236-294    _discord_start
   297-351    _ensure_discord_invite
  2356-2388   _ensure_error_channel
   422-435    _ensure_rank_roles
   674-688    _ensure_team_roles
  2456-2486   _error_channel_loop
   583-587    _guard
   503-531    _handle_voice_ai
   409-419    _is_admin
  1753-1764   _liveboard_loop
   590-608    _on_level_up
   499-500    _par_chat_id
  1837-1855   _post_clip_of_week
  1767-1785   _post_weekly_digest
   438-464    _provision_base_channels
   467-483    _provision_user_channels
  1306-1399   _reg_betrieb
   996-1085   _reg_community_setup
  1088-1163   _reg_daily_profil
  1206-1303   _reg_frage_events
   768-824    _reg_info
   942-993    _reg_moderation
  1166-1203   _reg_profil
   891-939    _reg_rollen
   827-888    _reg_server
  1402-1489   _reg_streamer
  1492-1537   _reg_system
   702-765    _reg_tracking
   643-671    _run_tg_handler
   486-496    _tracked_usernames
   153-215    _uebernehmen
  1717-1750   _update_liveboard
  1788-1802   _weekly_digest_loop
   218-221    starte
```

## Top-Level-Symbole in bot.py (533 Funktionen, 2 Klassen)

```
 24618-24640  _abbruch_datenbank_unlesbar
  2636-2637   _abo_key
  2657-2675   _abo_probe_dump
 24733-24751  _abschluss
 15768-15775  _ad_allowlist
 16748-16754  _agent_for
 16757-16773  _ai_telemetry
 17270-17288  _alert
 20718-20768  _alert_monitor_loop
 21120-21182  _announce_loop
  3515-3525   _anthropic_key
  3532-3534   _anthropic_model
  9618-9621   _arg_int
  2628-2633   _as_dict
 24368-24377  _async_exc_handler
 17451-17473  _audio_tap_cmd
 18031-18090  _audio_tap_melden
 17487-17511  _audio_tap_sammler
  8969-9002   _aufnahme_beim_stopp_sichern
 23668-23670  _aufnahme_deckel
  9005-9023   _aufnahme_platz_frei
 24700-24720  _aufnahmen_abschliessen
 24643-24697  _aufraeumen
  9789-9858   _auth_cookie
  9756-9785   _auth_guard
  1881-1886   _auto_on
 18707-18725  _auto_restream_loop
 13518-13560  _avatar_frames_laden
 22203-22218  _azrael_broadcast_reply
 22103-22125  _azrael_chat_reply
 22075-22100  _azrael_chat_should_reply
 22131-22133  _azrael_gate_cfg
 16778-16792  _azrael_live_state
 19744-19758  _azrael_overlay_state
 17152-17206  _azrael_proactive_loop
 16596-16652  _azrael_reaction_to_chats
 22136-22143  _azrael_reply_all_chats
 22062-22072  _azrael_self_names
 22171-22200  _azrael_send_to
 13479-13515  _azrael_spricht
 13822-13835  _azrael_stimme_stumm
 16798-16819  _azrael_system
 20852-20855  _backup_active
 20933-20946  _backup_loop
 23757-23761  _betrieb
 24441-24450  _brain_crowdsec_snap
 20639-20648  _brain_growth_loop
 10180-10207  _brain_growth_snapshot
  2564-2584   _brain_hint_delay
 24513-24548  _brain_moderation_snap
  6411-6439   _brain_notify
 24551-24573  _brain_recording_snap
 24453-24510  _brain_restream_health
 24576-24589  _brain_tiktok_status_snap
 11476-11493  _browser_push
  6451-6538   _build_daily_summary
 13869-13873  _build_restream_cmd
  5233-5260   _can_stop_tracking
  1994-2016   _capture_set_cookies
 12156-12159  _cfg_get
 12162-12164  _cfg_set
 19468-19503  _channel_set_all
 12707-12710  _chat_connected
 12713-12729  _chat_disconnected
  8612-8623   _chat_is_forum
 17838-17863  _chat_listener_abbauen
 12749-12751  _chat_sanitize
 12692-12704  _chat_stat
 12732-12735  _chat_stats_snapshot
  3827-3839   _check_ai_models_sync
 10462-10505  _classify_pool_anonymity
 10508-10525  _classify_pool_anonymity_bg
   877-899    _claude_chat_sync_metered
  9650-9657   _client_ip
 21266-21293  _clip_prune
 21296-21306  _clip_recfile_for
 21719-21725  _clip_should_velocity
 21348-21430  _clip_to_discord
  3713-3722   _close_ai_session
 22249-22264  _cohost_broadcast
 22234-22235  _cohost_cfg
 22290-22302  _cohost_fire_highlight
 22238-22246  _cohost_gate
 22267-22287  _cohost_highlight
 10110-10112  _conv_messages
  6810-6871   _cookie_alarm_loop
  2084-2085   _cookie_autofetch_info
  2068-2072   _cookie_autorefresh_info
 24078-24100  _cookie_bezug_loop
 24103-24128  _cookie_bezug_runde
  1971-1975   _cookie_header
  2097-2111   _cookies_selbst_holen
  4063-4075   _create_index_safe
 20190-20296  _crowdsec_status
 20136-20187  _crowdsec_via_lapi
 20040-20058  _cscli_bin
 20067-20080  _cscli_path
  6700-6725   _daily_summary_loop
 20098-20115  _darf_journal_lesen
  3049-3074   _darf_ytdlp_nachschlagen
 11657-11678  _dashboard_adresse
 20692-20715  _db_maintenance_loop
  6669-6697   _db_vacuum_loop
 15791-15815  _detect_foreign_ad
  1562-1573   _diag_path_owner
 17057-17102  _director_finalize
 18020-18027  _director_for
 17006-17054  _director_mark
 21582-21585  _disc_state_get
 21588-21595  _disc_state_set
 20620-20629  _discord_bot_starten
 20583-20594  _discord_einladung_merken
 20632-20636  _discord_invite
 20597-20617  _discord_kontext
 21543-21579  _discord_live_thread
 17209-17221  _discord_notify
 20555-20580  _discord_ops_alert
 21441-21539  _discord_post_user
 21185-21191  _discord_stop
  6728-6805   _disk_alarm_loop
 24003-24052  _disk_autoclean
 24223-24236  _disk_guard_loop
 13457-13464  _drossel_hoeher
 13453-13454  _drossel_stufe
 13467-13475  _drossel_zuruecksetzen
 11834-11836  _dump_all_threads
 10388-10451  _enrich_proxies_with_geo
  2140-2201   _ensure_cookie_file_netscape
  8671-8674   _ensure_notify_topic
 10632-10669  _ensure_proxy_ready
  8625-8652   _ensure_topic
   726-728    _env_int
   731-733    _env_int_range
 17254-17267  _event_webhook
 12507-12520  _evolution_loop
  5853-5887   _extract_file_payload
  2273-2275   _extract_urls_from_streamurl_node
 20083-20090  _f2b_sudo_hint
 24754-24817  _fatal_vom_botteil
 23673-23688  _fd_grenze_anheben
  4697-4707   _fehler_text
 10289-10307  _fetch_proxy_list
 17807-17835  _fetch_tiktok_room_id
   809-812    _ff_cmd
 13286-13291  _find_chromium
  3435-3437   _find_external_recorder
  2278-2280   _find_stream_urls
 12207-12232  _fire_webhooks
  7637-7646   _fork_safe
   910-923    _freeai_chat_sync_metered
 20129-20133  _geo_lookup_ips
  3701-3710   _get_ai_session
  7470-7510   _get_live_info
  2902-2909   _get_resolve_semaphore
  7919-8309   _handle_single_tracking
 23825-23827  _hb
 23830-23847  _hb_while
 12763-12765  _highlight_cfg
 12768-12797  _highlight_observe
 13294-13312  _htmlov_screenshot_cmd
 17513-17523  _httpx_proxy
 12240-12252  _in_quiet_hours
 24604-24615  _init_db_oder_abbruch
 25399-25430  _install_fast_eventloop
  9513-9567   _install_fast_json
 11839-11855  _install_faulthandler
 18753-18762  _intel_ensure_schema
 18805-18840  _intel_index_loop
 18774-18789  _intel_index_one
 18765-18771  _intel_semantic
  5222-5231   _is_authorized
  7820-7826   _is_dead
  2263-2265   _is_hevc
 20118-20120  _is_private_ip
  1780-1787   _is_process_running
  6441-6448   _is_quiet_hours
  1355-1364   _is_upload_window
  4562-4577   _iso
  9602-9615   _json_error_handler
  6663-6664   _kick_broadcaster_id
  6575-6617   _kick_follower_count
  6559-6562   _kick_slug
 11289-11296  _kick_user_token
 24592-24601  _kickmod_boot
  4152-4155   _kind_from_filename
 12269-12271  _latest_popularity
  1717-1726   _laufstand
 24186-24220  _laufstand_loop
 23764-23795  _leistung_erheben
 18416-18465  _live_react_loop
 18093-18405  _live_react_worker
  3285-3397   _live_status_aufloesen
 16655-16666  _live_transcript_push
 18407-18414  _live_users
 17105-17149  _living_title_loop
 20858-20930  _local_backup_scan
  9584-9598   _log_5xx
 23798-23822  _log_schleuse_pruefen
   799-806    _log_sicher
 13881-13893  _looks_like_codec_err
 13876-13878  _looks_like_source_expired
  7687-7717   _loop_fehler
 11859-11868  _loop_heartbeat
 23579-23612  _loop_lag_monitor
 23626-23646  _loop_stockung_melden
 23649-23659  _loop_takt_starten
 11871-11939  _loop_watchdog_thread
 16535-16549  _loyalty_add
 16526-16532  _loyalty_get
 16552-16560  _loyalty_top
 12379-12381  _manual_donations_total
  4904-4923   _manual_status
  7828-7829   _mark_dead
 10908-10924  _marketing_loop
 22150-22168  _maybe_handle_command
 24322-24346  _maybe_hype_clip
 21235-21263  _meme_klassifizieren
  4030-4053   _migrate_columns
 22429-22440  _mod_is_exempt
 22443-22448  _mod_warn_first
 22451-22454  _mod_warn_text
 12547-12555  _modlog
  1055-1057   _multistream_targets
  3077-3113   _nachschlag_ytdlp
  7649-7650   _nc_create_subprocess_exec
  7653-7654   _nc_create_subprocess_shell
 11226-11243  _news_loop
 12574-12576  _normalize_ingest
  2495-2512   _note_check_duration
  8665-8668   _notify_topic_name
  3116-3136   _ohne_url_melden
 16681-16689  _oracle_memories
 16955-16989  _oracle_memorize
 16692-16705  _oracle_persona
 16674-16678  _oracle_recent_text
 12920-12921  _ov_atomic_write
 12911-12913  _ov_bar
 15694-15706  _ov_clip_text
 12916-12917  _ov_oneline
 19795-19824  _overlay_push
 13240-13283  _overlay_render_size
 12643-12647  _overlay_session_reset
 19760-19762  _overlay_src_ok
 15778-15788  _own_invites
 13235-13237  _parse_size
 20304-20384  _parse_ssh_attacks
  7072-7105   _pause_resume_cmd
  2022-2066   _persist_refreshed_cookies
  1925-1957   _pick_checked_pull_proxy
  9686-9699   _pin_auth_value
  9745-9746   _pin_clear_fail
  9725-9728   _pin_locked
  9731-9742   _pin_note_fail
  9702-9722   _pin_ok
 19604-19629  _piper_pick_model
 19689-19738  _piper_say
 12169-12204  _post_json_threaded
 13214-13232  _probe_video_size
  1808-1825   _proc_is_recorder
 10601-10629  _proxy_pool_refresh_loop
  1891-1922   _proxy_report_recording
 23708-23719  _pruefung_verworfen
 11824-11826  _prune_stall_dumps
 10978-11148  _public_stats
  2088-2094   _pull_proxy_still
 17225-17251  _push_notify
  9905-9907   _pwa_dir
 10358-10373  _quick_validate_proxy
 12235-12237  _quiet_hours_config
  9870-9903   _rate_guard
 16496-16502  _react_warn
  7557-7596   _reap_proc
  8899-8966   _rec_auto_abschalten
  8846-8896   _rec_frueh_getrennt
  8729-8791   _rec_kategorie_melden
  8794-8843   _rec_totstreak_fortschreiben
  2535-2557   _record_check_outcome
   794-796    _redact_stream_urls
 10528-10598  _refresh_proxy_pool
  2312-2403   _resolve_via_html
  2682-2879   _resolve_via_webcast_api_v2
  2942-3025   _resolve_via_ytdlp
 21759-21888  _resolve_youtube_ingest
  2289-2309   _resolver_stumm
 12626-12637  _restream_active_sources
 13563-13687  _restream_avatar_feeder_start
 13690-13699  _restream_avatar_feeder_stop
 17866-17984  _restream_chat_guardian
 12800-12872  _restream_chat_push
 12897-12906  _restream_chat_push_async
 13315-13424  _restream_html_overlay_start
 13427-13440  _restream_html_overlay_stop
 12585-12608  _restream_overlay_files
 18469-18501  _restream_platform_state
 18669-18704  _restream_resume_after_restart
 13747-13819  _restream_tts_enqueue_wav
 13176-13208  _restream_tts_feeder
 13173-13174  _restream_tts_fifo_path
 13702-13729  _restream_tts_start
 13731-13745  _restream_tts_stop
 18507-18666  _restream_verify_loop
 20823-20835  _retention_loop
 20817-20820  _retention_scan
  2639-2641   _room_is_abo
  5891-6008   _run_ai_call
 11962-11975  _run_async_from_flask
 20123-20126  _run_priv
 25387-25395  _run_selfcheck_and_exit
 20838-20849  _s3_client
  7855-7906   _safe_send
  4830-4846   _sample_net_throughput
  2587-2614   _schedule_next_check
 20771-20814  _scheduler_loop
  4056-4060   _schema_pk
 11979-11984  _scraper_session
 22457-22496  _screen_full
 11340-11377  _sec_headers
  2268-2270   _select_stream_from_data_section
 25107-25384  _selfcheck
  8677-8711   _send_live_notice
  1378-1382   _should_defer_upload
 21309-21345  _shrink_for_discord
  9910-9922   _sicheres_ziel
 20651-20689  _sicherheits_erinnerung_loop
 24243-24260  _sign_health_check
 24263-24282  _sign_health_loop
  4580-4605   _sitzung_bestimmen
  7666-7677   _spawn
 25812-25842  _spawn_from_flask
 23722-23728  _speicher_maps
 23731-23746  _speicher_pflegen
 17525-17804  _start_chat_listener
 23691-23705  _start_gesperrt
 11942-11959  _start_loop_watchdog
 11175-11221  _stats_loop
 11154-11157  _stats_output_path
 11160-11172  _stats_write
 19641-19655  _stimme_saubern
 19662-19686  _stimme_schon_gesagt
  8388-8404   _storage_cleanup_loop
 24302-24309  _story_for
  3460-3466   _stream_url_expiry
  3468-3473   _stream_url_ttl
 15741-15748  _streamer_persona_get
 20955-21077  _system_backup
 21086-21116  _system_backup_loop
 11784-11802  _task_auf_bot_schleife
 23270-23286  _telegram_befehlsmenue
  7720-7766   _telegram_polling_fehler
 10310-10349  _test_proxy
 10856-10872  _testpush_resolve_live
  7831-7852   _tg_sprache_setzen
  8584-8594   _tg_topics_load_into_mem
  8581-8582   _tg_topics_path
  8596-8603   _tg_topics_save
  9660-9668   _token_ok
  8606-8610   _topic_forget
 12255-12266  _tracking_max_duration
  4360-4374   _tracking_remove_cleanup
  4391-4403   _tracking_resume_cleanup
  1620-1643   _try_attach_file_handler
 19631-19639  _tts_cleanup
 10832-10836  _tunnel_effective
 24055-24075  _tunnel_lage
 24131-24183  _tunnel_wacht_loop
 19127-19180  _twitch_channel_status
 22499-22644  _twitch_chat_loop
 21601-21614  _twitch_clip_versuchen
 22313-22416  _twitch_eventsub_loop
  1401-1414   _upload_queue_add
  1425-1427   _upload_queue_count
  1384-1393   _upload_queue_load
  1374-1376   _upload_queue_path
  1416-1423   _upload_queue_remove
  1395-1399   _upload_queue_save
  1429-1470   _upload_window_loop
  7530-7537   _uptime_s
 12562-12571  _url_host
  3139-3233   _url_nachschlag
   870-874    _usage_record_claude
 24416-24438  _v37_pause_source
 24380-24390  _v37_restream_restart
 24393-24413  _v37_unpause_source
  7769-7813   _verbindung_verloren
  6620-6651   _viewer_sample_loop
  9749-9752   _wants_html
  7540-7554   _warn_empty_env
 23868-23989  _watchdog_loop
 22034-22042  _wchat_thank_ok
 17293-17323  _whisper_get_model
  7627-7634   _whisper_native_section
 16483-16489  _whisper_pool
 17417-17449  _whisper_segments
 17325-17341  _whisper_stumm
 17344-17414  _whisper_transcribe
 12968-13130  _write_restream_overlay
 12930-12965  _write_restream_overlay_async
 22668-22764  _youtube_api_chat_loop
 19183-19286  _youtube_api_status
 19289-19356  _youtube_channel_status
 22767-22928  _youtube_chat_loop
 21617-21642  _youtube_clip_versuchen
 21894-21907  _youtube_restream_autoconfig
 21910-21934  _youtube_restream_autoconfig_inner
 22001-22029  _youtube_send
 19424-19465  _youtube_set_channel
 21937-21971  _yt_access_token
 21974-21989  _yt_live_chat_id
 21997-21998  _yt_sendrate_cfg
 22647-22662  _yt_timeout
  2926-2927   _ytdlp_detect_available
  2929-2940   _ytdlp_note_result
 11829-11831  _zombie_child_count
  7406-7430   about
  4271-4275   add_ai_log_entry
  4188-4191   add_archive_entry
  4868-4870   add_archive_rule
  4608-4679   add_recording
  4335-4352   add_tracking
  6011-6044   ai
  3853-3934   ai_chat
  3968-3978   ai_history_append
  3980-3985   ai_history_clear
  3957-3966   ai_history_load
  3942-3955   ai_rate_limit_check
  6073-6081   aireset
 16822-16841  azrael_chat
 22933-23055  brain_cmd
  3476-3481   build_recording_cmd
  4355-4358   bulk_add_trackings
  6874-6933   bulkadd
  8407-8564   check_all_trackings
  4407-4419   claim_live_transition
 15818-16415  class KickModerator
 13896-15581  class RestreamManager
 10715-10757  classify_proxy_anonymity
  6119-6317   cleanup
  5158-5164   cleanup_old_recordings
  4553-4560   clear_recording
 21645-21716  clip_moment
  4820-4823   compute_storage_forecast
  6996-7069   cookies_cmd
  4326-4332   count_trackings_for_chat
  4258-4269   decide_preferred_recorder
  4198-4201   delete_archive_entry
  4872-4874   delete_archive_rule
  5548-5695   diag
 23167-23228  einnahmen_cmd
  4814-4817   find_recordings_by_fingerprint
  4219-4235   finish_recording_attempt
  4379-4381   get_all_active_trackings
  4286-4288   get_all_checks
  4681-4684   get_all_recordings
  4763-4765   get_all_tags_with_counts
  4791-4794   get_annotations_for_recording
  4193-4196   get_archive_entry
  4784-4787   get_bookmarked_recordings
  2128-2133   get_cookie_health
  4751-4757   get_event_log
  4242-4256   get_last_recording_attempt
  3236-3278   get_live_status
  5097-5100   get_manual_recordings
  4799-4802   get_or_compute_inspect_sync
  5199-5202   get_outcome_breakdown
  4770-4773   get_priority_poll_interval
  4237-4240   get_recent_recording_attempts
  4686-4689   get_recording_by_id
  4777-4780   get_recording_note
  3647-3670   get_redis
  4315-4318   get_stats
  5152-5156   get_storage_stats
  4892-4894   get_tiktok_status_distribution
  4421-4430   get_tracking_state
  4376-4377   get_trackings_for_group
  5113-5116   get_trash_recordings
  9026-9492   handle_recording_finished
 23262-23267  hilfe_cmd
  4083-4143   init_db
  4864-4866   list_archive_rules
  5352-5390   live
  7909-7917   live_check_worker
  3725-3764   llm_chat
  3787-3817   llm_chat_sync
  3772-3784   llm_list_models
  4710-4743   log_event
  1742-1775   log_recording_failure
  7219-7268   logs_cmd
 24820-25097  main
  6047-6070   on_ai_media
  7345-7371   on_ai_reply
  7374-7403   on_azrael_mention
  7435-7465   on_callback
 16847-16952  oracle_handle
  7108-7111   pause_tracking
  5212-5217   profile_keyboard
  7170-7216   quota
  8311-8385   reaper_loop
  4888-4890   record_tiktok_status
  6086-6116   recstatus
  3672-3680   redis_get_json
  3683-3689   redis_set_json
 23289-23299  report_cmd
 10760-10762  report_proxy_result
  2406-2448   resolve_tiktok_live_stream
  5108-5111   restore_recording
  7114-7117   resume_tracking
  4877-4882   run_archive_rules
 23302-23559  run_bot
 11681-11775  run_flask
  4852-4855   sample_bandwidth_for_active
  4278-4284   save_tiktok_check
  4545-4551   set_recording_file
  4384-4388   set_tracking_paused
  5103-5106   soft_delete_recording
  8717-8727   split_and_send_video
  5265-5307   start
  4203-4217   start_recording_attempt
  6320-6358   stats
  5042-5095   stop_manual_recording
  7120-7167   stoprec
  6544-6552   summary_cmd
  7271-7342   sysres
  5697-5841   teststream
  5309-5350   tiktok
  6936-6993   topusers
  5427-5484   track
  5392-5424   track_exact
  5498-5546   tracklist
  4926-5040   trigger_manual_recording
  4506-4543   try_acquire_recording_lock
  5119-5121   universal_search
 23231-23259  unpause_cmd
  5486-5496   untrack
 23058-23164  update_cmd
  4809-4812   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, class BestandUnbekannt, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, finde_ohne_eintrag, get_archive_entries_paged, get_archive_entry, run_archive_file_check, uebernehmen
archivename.py         open_unique
archiverules.py        add_archive_rule, delete_archive_rule, list_archive_rules, run_archive_rules
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
audiocue.py            config, configure
audiotap.py            diagnose, melden, warum_kein_tap
aufnahmefolge.py       aufnahme_geglueckt, daten_geflossen, melden_erlaubt, nach_403, nach_frueher_trennung, nach_totem_versuch, sitzung_zuende, sperre_rest, stall_grenze
aufnahmekategorie.py   kategorisiere
aufnahmesitzung.py     abdeckung, angleich_cmd, braucht_angleich, concat_cmd, concat_liste, gehoert_dazu, luecken, probe_cmd, sekunden, sitzung_id, tonformat, zieldatei
auslieferung.py        schreibe, stand, text
avatarloop.py          blinzeln, ruhe_seit, schleife, zustand
azraelstate.py         configure, flag, haken, personas_load, personas_path, personas_save
backupcfg.py           aktiv, fehlgrund, lokal, lokal_dir, recordings_retain_days, retention_days, s3, s3_bucket, s3_endpoint, s3_konfiguriert, s3_region, s3_zugang, sys_backup, sys_hour, sys_keep, sys_max_file_mb
badwords.py            banned_path, configure, fetch_ldnoobw_de, learned_path, load_banned, load_learned, save_banned, save_learned
bandbreite.py          messen
befehle.py             beschreibung, discord_nativ, discord_ueber_tg, fuer, hilfe_text, pruefen, telegram_handler
betriebslage.py        bereit, bewerten, sichern_beim_stopp
binresolve.py          resolve
botctx.py              class BotKontext
brainstate.py          history_for, record, stall, stream_recent
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
chatfolge.py           entscheide
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           anzeigename, configure, darf_pingen, highlight_post, highlight_share_enabled, live_ping, live_ping_enabled, note_chatter, returning_enabled, rollen_id, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookiebezug.py         anstossen, configure, faellig, gast_hilft, holen, info, intervall_s, naechster_lauf
cookieholen.py         aktualisiere, aus_browser, configure, hole_gastcookies, schreibe, zusammenfuehren
cookies.py             configure, gesundheit, lade_jar, load_dict
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, erwartete_namen, fehlende_namen, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dashauth.py            erlaubt_offen, geschuetzt, host, lage, nur_lokal, offen_im_netz, zurueckgefallen
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbrestore.py           archive, dump_aus_archiv, einsetzen, einspielen, vorbereiten
dbwrap.py              class DatenbankUnlesbar, configure_db, datei_diagnose, db_async, db_conn, get_pool, set_pool
ddlsafe.py             ddl, ist_schon_da
defensecfg.py          bouncer_gesetzt, bouncer_key, geo_fehler, geo_fehler_setzen, lapi_host, lapi_port, lapi_url, server_lat, server_lon
director.py            class LiveDirector, configure
discordlimits.py       aktuell_label, aktuell_mb, configure, describe, effective_upload_mb, gate_mb, guild_filesize_bytes, guild_limit_mb
discordrang.py         rang_fuer_level, slug, xp_fuer_level, xp_zu_level
discordstate.py        invite, state_get
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
donationsdb.py         manual_rows, manual_total, parse_eur
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventlog.py            leeren, schreibe, stand
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, write_build
fehlertext.py          nach_aussen, saeubern
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      anzeige_groesse, avatar_kette, chat_umbruch_w, chat_zeilen, drawtext_chain, studio_chain, studio_masse
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, dienstmeldung, katalog_kennt, last_errors, list_models_sync, stream_haeppchen, stream_rest
gegendruck.py          abgewiesen, deckel_auto, fd_grenze_anheben, fd_lage, freigeben, lage, reservieren, reserviert, start_entscheiden, verworfen, zuruecksetzen
geocache.py            get, groesse, leeren, put
geoip.py               ist_privat, lookup
highlights.py          check, new_state, observe, score, zustand
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kennzahlen.py          prometheus, prozess, stand, veroeffentlichen, zeile
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
kickapi.py             app_token, broadcaster_id, channel_info, configure, oauth_exchange, search_category, send_message, slug, timeout_user, update_channel, user_token
kindprozess.py         alle_beenden, ausfuehren, beenden, lage, zuruecksetzen
kiwahl.py              backend, lokal_stand, lokal_zuerst, normal, provider
lagebild.py            bauen, restream_lage
lastvorsorge.py        freie_kerne, jung, startstufe
laufstand.py           befehl, veraltet, vergleich
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
livecache.py           aufraeumen, aufraeumen_faellig, dauer, einflug, frisch, holen, setzen, statistik, zaehle, zaehler_zuruecksetzen
livefolge.py           braucht_url_nachschlag, hat_stream_url, last_dehnung, live_gesehen, offline_bestaetigt, poll_abstand, ruhezeit
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             fuer_log, redact_cookie_zeilen, redact_pull_urls, redact_stream_urls, url_ohne_zugang
logschleuse.py         class Schleuse, entkoppeln, nachziehen, stoppen, synchrone_handler, verloren, wartend, zuruecksetzen
looplag.py             bremser, erfassen, lage, spaeher_starten, stelle_aus_rahmen, takt, zuruecksetzen
loyalty.py             award_chat, award_return, configure, enabled, leaderboard, rank_for, status
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
meldetakt.py           melden, zuruecksetzen, zusatz
memeklip.py            class Fenster, frage, lies_urteil, soll_clippen
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
modki.py               frage, lies_klassifikation, lies_schimpfwoerter
modstats.py            ist_moderation, plattform, quellen, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
outcomes.py            get_outcome_breakdown
overlaytext.py         configure, latest_popularity, ov_atomic_write, ov_bar, ov_oneline, overlay_src_ok
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
qrsvg.py               qr_svg
reccmd.py              build_recording_cmd, configure
recdb.py               configure, find_recordings_by_fingerprint, get_all_checks, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
resolvergrund.py       http_grund, quelle_lage, quelle_laut, text
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, fenstergroesse, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, url_host
restreamcfg.py         active_platforms, aktiv, bereite_ziele, bruecke, bruecke_luecke, bruecke_offline, chat_src_ok, discord_invite, enabled, ingest, key_gesetzt, kick_channel_url, overlay, stall_timeout, verify, verify_karenz, verify_misses, verify_takt, yt_oauth_configured, ziel
restreamcmd.py         build, configure, drossel_avatar_aus, drossel_bitrate, drossel_canvas, drossel_fps, drossel_preset, drossel_zusatz, fueller, quell_eingang, schriftart, zubringer
restreamgesundheit.py  blind_markieren, frische_tee_fehler, marke_setzen
restreamstate.py       guard, haken, laufende, layout_mode, mgr
restrend.py            rising_trend
retention.py           scan
revenue.py             is_revenue_platform, normalisieren, sql_in
schema.py              create_schema
schemastand.py         lege_an, lies, pruefe, schreibe, streng
schnappschuss.py       class Schnappschuss
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendebruecke.py        class Bruecke, class TsUmschreiber, ist_keyframe, pat_pmt_pid, pes_zeit, pid, pmt_stroeme, pmt_urteil, video_pid
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sicherpfad.py          pruefe_unter, sicher_join, sicherer_name, unter
speicherpflege.py      abgelaufene_weg, alte_stempel_weg, groessen
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
storage.py             cleanup, forecast, stats
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
suche.py               universal_search
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
systemprobe.py         active_recorder, ai_alive, ai_calls_total, cache_leeren, cached_probe, configure, cpu_load_snapshot, disk_pct, recorder_pref, recordings_dir, redis_alive, redis_url, redis_version
telegramfehler.py      dauer_text, grund, ist_fehler, text, zuruecksetzen
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tiktokcheck.py         account_exists, configure
tiktokheaders.py       configure
tonspur.py             class Fehlschlag, garantie, garantie_cmd, hat_ton, hat_tonspur, ist_tonlos_fehler, nachruest_cmd, pruef_cmd, pruefen, sichern, stille_eingabe
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
tunnelwacht.py         lage, meldung, probe, probe_cmd
twitchoauth.py         access_token, authorize_url, configure, create_clip, exchange_code, forget, login_name, search_category, status, timeout_user, update_channel
updater.py             build_plan, check, class Plan, class UpdaterConfig, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             build_stamp, changelog, current, latest, summary_line
videoteil.py           configure, dauer, ist_kaputter_container, kopier_teilen, neu_kodieren, platz_reicht, reparieren, wegwerfen, zeitstempel_richten, zu_gross
webserver.py           bindung, ist_loopback, schema, threads, tls_lage, waehle
whispercfg.py          geladen, name, verfuegbar, waehle
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytdlpurl.py            urls_aus_json
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status, upload_clip
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DiskAgent, class HealthAgent, class LearningAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler
semantic.py            class SemanticMemory
state.py               class Entity, class StateMachine
test_bughunt.py        db_conn, main
test_m1.py             main
test_m3.py             main
test_m4.py             main
test_m5.py             main
test_m6.py             class LlamaCppMock, main
test_m7.py             db_conn, main
```
