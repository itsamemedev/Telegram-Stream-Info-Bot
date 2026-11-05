# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
 10155  GET              /                                                dashboard
 12210  GET              /api/abo/status                                  api_abo_status
 12164  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 10943  GET              /api/automation/status                           api_automation_status
 10965  POST             /api/automation/toggle                           api_automation_toggle
 19792  GET              /api/channel/categories                          api_channel_categories
 19798  POST             /api/channel/set                                 api_channel_set
 19645  GET              /api/channels/status                             api_channels_status
 19319  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 19302  GET              /api/clips                                       api_clips
 19348  POST/DELETE      /api/clips/clear                                 api_clips_clear
 19220  GET              /api/debug/threads                               api_debug_threads
 12175  GET              /api/events                                      api_events
 11654  GET              /api/events/stream                               api_events_stream
 11481  GET              /api/health                                      api_health
 19261  POST             /api/highlights/config                           api_highlights_config
 10089  POST             /api/login                                       dashboard_login_submit
 12500  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 11569  GET              /api/notify/status                               api_notify_status
 11580  POST             /api/notify/test                                 api_notify_test
 12264  GET              /api/proxy/heatmap                               api_proxy_heatmap
 12241  GET              /api/proxy/trend                                 api_proxy_trend
 19368  GET              /api/tts/<fn>                                    api_tts_file
 20145  GET              /api/upload_window                               api_upload_window
 11771  GET              /archive/<int:eid>/download                      archive_download
 11799  GET              /download/<int:recording_id>                     download
 11728  GET              /health                                          health
 19129  GET              /healthz                                         healthz
 10080  GET              /login                                           dashboard_login_page
 10110  GET              /logout                                          dashboard_logout
 10117  GET              /manifest.webmanifest                            pwa_manifest
 20118  GET              /overlay                                         overlay_page
 10141  GET              /pwa-icon-<variant>.png                          pwa_icon
 10127  GET              /sw.js                                           pwa_service_worker
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
   341  GET              /api/backoff-watch                               api_backoff_watch   [nc/routes/beobachtung.py]
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
   266  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   548  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   523  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
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
   536  GET              /api/stream/inspect/<username>                   api_stream_inspect   [nc/routes/beobachtung.py]
   395  GET              /api/stream/timeline                             api_stream_timeline   [nc/routes/beobachtung.py]
   425  GET              /api/stream/transcript                           api_stream_transcript   [nc/routes/beobachtung.py]
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
   239  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   460  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   489  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   409  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   422  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   518  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   395  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   270  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   315  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   339  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   326  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   166  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   284  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   136  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   376  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   431  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
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
   467  GET              /metrics                                         api_prometheus_metrics   [nc/routes/beobachtung.py]
```

## Discord-Slash-Commands in discordbot.py (66)

```
  2091  /about                  Ueber diesen Bot
   813  /ai                     
  2091  /aireset                KI-Kontext zuruecksetzen
  1222  /ask                    
   914  /assign_role            
   964  /ban                    
  2046  /botstats               
  2091  /brain                  Brain-Lage: Regeln, Agenten, Empfehlungen
  2091  /bulkadd                Mehrere User auf einmal tracken · a b c
  2091  /cleanup                Alte Aufnahmen aufraeumen
  1477  /clearwarns             
  2010  /clip                   
  1995  /clipoftheweek          
  1348  /clips                  
  2091  /cookies                Cookie-Status — mit 'holen' selbst beziehen · [holen]
   869  /create_category        
   840  /create_channel         
   904  /create_group           
   879  /create_role            
   855  /create_voice           
  1100  /daily                  
  2091  /diag                   Vollstaendige Diagnose
  2091  /einnahmen              Einnahmen und Spenden
  1251  /event                  
  1293  /events                 
  1387  /follow                 
  1376  /help                   
   954  /kick                   
  1075  /leaderboard            
  2091  /live                   Live-Status sofort pruefen · @user
  1335  /livenow                
  2091  /logs                   Letzte Fehler aus dem Log
  2091  /pause                  Tracking pausieren · @user
  1363  /post_test              
  1183  /profile                
   986  /purge                  
  2091  /quelle                 Stream-Quellen eines Live-Nutzers messen (alle Wege, ffprobe
  2091  /quota                  Speicher-Quota
  1062  /rank                   
  1323  /recstatus              
   924  /remove_role            
  2091  /report                 Azrael-Sentinel-Wochenreport
   826  /restream_status        
  2091  /resume                 Tracking fortsetzen · @user
   934  /set_channel_perms      
  1029  /setup_community        
  1046  /setup_targets          
  1419  /stats                  
   785  /status                 
  2091  /stoprec                Laufende Aufnahme sauber beenden · @user
  1515  /streaminfo             
  2091  /summary                Tageszusammenfassung
  2091  /sysres                 System-Ressourcen
  2091  /teststream             Recorder-Selbsttest · @user
  2091  /tiktok                 Profil-Analyse eines TikTok-Accounts · ‹name›
   974  /timeout                
  1487  /topstreamers           
  2091  /topusers               Top-Streamer nach Aufnahmen
   715  /track                  
  2091  /track_exact            Exakten Usernamen tracken (ohne Korrektur) · ‹name›
   798  /tracklist              
  1401  /unfollow               
  2091  /unpause                Auto-pausierte Quelle wieder aktivieren · @user
   747  /untrack                
  1440  /warn                   
  1463  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2249  on_member_join
  2211  on_message
  2112  on_raw_reaction_add
  2284  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    58-73     konfiguriere
    76-476    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (46 Funktionen)

```
  1592-1643   _award_xp
  1814-1843   _clip_week_leader
  1867-1881   _clipoftheweek_loop
  2400-2462   _community_events_loop
  1549-1571   _dc_client
  1574-1583   _dc_offen
  2502-2537   _disc_automod_check
   403-408    _disc_sprache_setzen
  1646-1694   _discord_ai_automod
   536-575    _discord_automod
  1697-1717   _discord_azrael_reply
  1884-2359   _discord_run_once
   238-296    _discord_start
   299-353    _ensure_discord_invite
  2365-2397   _ensure_error_channel
   424-437    _ensure_rank_roles
   678-692    _ensure_team_roles
  2465-2495   _error_channel_loop
   585-589    _guard
   505-533    _handle_voice_ai
   411-421    _is_admin
  1762-1773   _liveboard_loop
   592-610    _on_level_up
   501-502    _par_chat_id
  1846-1864   _post_clip_of_week
  1776-1794   _post_weekly_digest
   440-466    _provision_base_channels
   469-485    _provision_user_channels
  1315-1408   _reg_betrieb
  1000-1089   _reg_community_setup
  1092-1172   _reg_daily_profil
  1215-1312   _reg_frage_events
   772-828    _reg_info
   946-997    _reg_moderation
  1175-1212   _reg_profil
   895-943    _reg_rollen
   831-892    _reg_server
  1411-1498   _reg_streamer
  1501-1546   _reg_system
   706-769    _reg_tracking
   645-675    _run_tg_handler
   488-498    _tracked_usernames
   155-217    _uebernehmen
  1726-1759   _update_liveboard
  1797-1811   _weekly_digest_loop
   220-223    starte
```

## Top-Level-Symbole in bot.py (538 Funktionen, 2 Klassen)

```
 24951-24973  _abbruch_datenbank_unlesbar
  2648-2649   _abo_key
  2669-2687   _abo_probe_dump
 25069-25085  _abschied_wachen
 25088-25106  _abschluss
 16018-16025  _ad_allowlist
 17017-17023  _agent_for
 17026-17042  _ai_telemetry
 17539-17557  _alert
 21013-21063  _alert_monitor_loop
 21445-21507  _announce_loop
  3534-3544   _anthropic_key
  3551-3553   _anthropic_model
  9772-9775   _arg_int
  2640-2645   _as_dict
 24701-24710  _async_exc_handler
 17720-17742  _audio_tap_cmd
 18300-18359  _audio_tap_melden
 17756-17780  _audio_tap_sammler
  9121-9154   _aufnahme_beim_stopp_sichern
 23993-23995  _aufnahme_deckel
  9157-9175   _aufnahme_platz_frei
 25033-25053  _aufnahmen_abschliessen
 24976-25030  _aufraeumen
  9943-10012  _auth_cookie
  9910-9939   _auth_guard
  1890-1895   _auto_on
 18986-19004  _auto_restream_loop
 13712-13754  _avatar_frames_laden
 22528-22543  _azrael_broadcast_reply
 22428-22450  _azrael_chat_reply
 22400-22425  _azrael_chat_should_reply
 22456-22458  _azrael_gate_cfg
 17047-17061  _azrael_live_state
 20031-20045  _azrael_overlay_state
 17421-17475  _azrael_proactive_loop
 16865-16921  _azrael_reaction_to_chats
 22461-22468  _azrael_reply_all_chats
 22387-22397  _azrael_self_names
 22496-22525  _azrael_send_to
 13673-13709  _azrael_spricht
 14016-14029  _azrael_stimme_stumm
 17067-17088  _azrael_system
 21147-21150  _backup_active
 21228-21241  _backup_loop
 24082-24086  _betrieb
 24774-24783  _brain_crowdsec_snap
 20934-20943  _brain_growth_loop
 10334-10361  _brain_growth_snapshot
  2573-2593   _brain_hint_delay
 24846-24881  _brain_moderation_snap
  6476-6504   _brain_notify
 24884-24906  _brain_recording_snap
 24786-24843  _brain_restream_health
 24909-24922  _brain_tiktok_status_snap
 11633-11650  _browser_push
  6516-6603   _build_daily_summary
 14063-14067  _build_restream_cmd
  5229-5256   _can_stop_tracking
  2003-2025   _capture_set_cookies
 12318-12321  _cfg_get
 12324-12326  _cfg_set
 19753-19788  _channel_set_all
 12901-12904  _chat_connected
 12907-12923  _chat_disconnected
  8764-8775   _chat_is_forum
 18107-18132  _chat_listener_abbauen
 12943-12945  _chat_sanitize
 12886-12898  _chat_stat
 12926-12929  _chat_stats_snapshot
  3852-3864   _check_ai_models_sync
 10616-10659  _classify_pool_anonymity
 10662-10679  _classify_pool_anonymity_bg
   882-904    _claude_chat_sync_metered
  9804-9811   _client_ip
 21591-21618  _clip_prune
 21621-21631  _clip_recfile_for
 22044-22050  _clip_should_velocity
 21673-21755  _clip_to_discord
  3738-3747   _close_ai_session
 22574-22589  _cohost_broadcast
 22559-22560  _cohost_cfg
 22615-22627  _cohost_fire_highlight
 22563-22571  _cohost_gate
 22592-22612  _cohost_highlight
 10264-10266  _conv_messages
  6875-6936   _cookie_alarm_loop
  2093-2094   _cookie_autofetch_info
  2077-2081   _cookie_autorefresh_info
 24411-24433  _cookie_bezug_loop
 24436-24461  _cookie_bezug_runde
  1980-1984   _cookie_header
  2106-2120   _cookies_selbst_holen
  4068-4070   _create_index_safe
 20477-20591  _crowdsec_status
 20423-20474  _crowdsec_via_lapi
 20327-20345  _cscli_bin
 20354-20367  _cscli_path
  6765-6790   _daily_summary_loop
 20385-20402  _darf_journal_lesen
  3063-3088   _darf_ytdlp_nachschlagen
 11814-11835  _dashboard_adresse
 20987-21010  _db_maintenance_loop
  6734-6762   _db_vacuum_loop
 16041-16065  _detect_foreign_ad
  1571-1582   _diag_path_owner
 17326-17371  _director_finalize
 18289-18296  _director_for
 17275-17323  _director_mark
 21907-21910  _disc_state_get
 21913-21920  _disc_state_set
 20915-20924  _discord_bot_starten
 20878-20889  _discord_einladung_merken
 20927-20931  _discord_invite
 20892-20912  _discord_kontext
 21868-21904  _discord_live_thread
 17478-17490  _discord_notify
 20850-20875  _discord_ops_alert
 21766-21864  _discord_post_user
 21510-21516  _discord_stop
  6793-6870   _disk_alarm_loop
 24336-24385  _disk_autoclean
 24556-24569  _disk_guard_loop
 13651-13658  _drossel_hoeher
 13647-13648  _drossel_stufe
 13661-13669  _drossel_zuruecksetzen
 11991-11993  _dump_all_threads
 10542-10605  _enrich_proxies_with_geo
  2149-2210   _ensure_cookie_file_netscape
  8823-8826   _ensure_notify_topic
 10786-10823  _ensure_proxy_ready
  8777-8804   _ensure_topic
   726-728    _env_int
   731-733    _env_int_range
 17523-17536  _event_webhook
 12669-12682  _evolution_loop
  5918-5952   _extract_file_payload
  2282-2284   _extract_urls_from_streamurl_node
 20370-20377  _f2b_sudo_hint
 25109-25172  _fatal_vom_botteil
 23998-24013  _fd_grenze_anheben
  4693-4703   _fehler_text
 10443-10461  _fetch_proxy_list
 18076-18104  _fetch_tiktok_room_id
   809-812    _ff_cmd
 13480-13485  _find_chromium
  3454-3456   _find_external_recorder
  2287-2289   _find_stream_urls
 12369-12394  _fire_webhooks
  7702-7711   _fork_safe
   915-928    _freeai_chat_sync_metered
 20416-20420  _geo_lookup_ips
  3726-3735   _get_ai_session
  7535-7575   _get_live_info
  2914-2921   _get_resolve_semaphore
  8027-8417   _handle_single_tracking
 24158-24160  _hb
 24163-24180  _hb_while
 12957-12959  _highlight_cfg
 12962-12991  _highlight_observe
 13488-13506  _htmlov_screenshot_cmd
 17782-17792  _httpx_proxy
 12402-12414  _in_quiet_hours
 24937-24948  _init_db_oder_abbruch
 25755-25786  _install_fast_eventloop
  9667-9721   _install_fast_json
 11996-12012  _install_faulthandler
 19032-19041  _intel_ensure_schema
 19084-19119  _intel_index_loop
 19053-19068  _intel_index_one
 19044-19050  _intel_semantic
  5218-5227   _is_authorized
  7913-7934   _is_dead
  2272-2274   _is_hevc
 20405-20407  _is_private_ip
  1789-1796   _is_process_running
  6506-6513   _is_quiet_hours
  1364-1373   _is_upload_window
  4558-4573   _iso
  9756-9769   _json_error_handler
  6728-6729   _kick_broadcaster_id
  6640-6682   _kick_follower_count
  6624-6627   _kick_slug
 11446-11453  _kick_user_token
  7834-7859   _kick_ws_pause
 24925-24934  _kickmod_boot
  4148-4151   _kind_from_filename
 12431-12433  _latest_popularity
  1726-1735   _laufstand
 24519-24553  _laufstand_loop
 24089-24120  _leistung_erheben
 18695-18744  _live_react_loop
 18362-18684  _live_react_worker
  3304-3416   _live_status_aufloesen
 16924-16935  _live_transcript_push
 18686-18693  _live_users
 17374-17418  _living_title_loop
 21153-21225  _local_backup_scan
  9738-9752   _log_5xx
 24123-24155  _log_schleuse_pruefen
   799-806    _log_sicher
 14075-14087  _looks_like_codec_err
 14070-14072  _looks_like_source_expired
  7752-7782   _loop_fehler
 12016-12025  _loop_heartbeat
 23904-23937  _loop_lag_monitor
 23951-23971  _loop_stockung_melden
 23974-23984  _loop_takt_starten
 12028-12101  _loop_watchdog_thread
 16801-16818  _loyalty_add
 16792-16798  _loyalty_get
 16821-16829  _loyalty_top
 12541-12543  _manual_donations_total
  4900-4919   _manual_status
  7936-7937   _mark_dead
 11062-11078  _marketing_loop
 22475-22493  _maybe_handle_command
 24655-24679  _maybe_hype_clip
 21560-21588  _meme_klassifizieren
  4055-4060   _migrate_columns
 22754-22765  _mod_is_exempt
 22768-22773  _mod_warn_first
 22776-22779  _mod_warn_text
 12726-12745  _modlog
 12709-12723  _modlog_schreiben
  1060-1062   _multistream_targets
  3091-3127   _nachschlag_ytdlp
  7714-7715   _nc_create_subprocess_exec
  7718-7719   _nc_create_subprocess_shell
 11383-11400  _news_loop
 12768-12770  _normalize_ingest
  2504-2521   _note_check_duration
  8817-8820   _notify_topic_name
  3130-3150   _ohne_url_melden
 16950-16958  _oracle_memories
 17224-17258  _oracle_memorize
 16961-16974  _oracle_persona
 16943-16947  _oracle_recent_text
 13114-13115  _ov_atomic_write
 13105-13107  _ov_bar
 15944-15956  _ov_clip_text
 13110-13111  _ov_oneline
 20082-20111  _overlay_push
 13434-13477  _overlay_render_size
 12837-12841  _overlay_session_reset
 20047-20049  _overlay_src_ok
 16028-16038  _own_invites
 13429-13431  _parse_size
 20599-20679  _parse_ssh_attacks
  7137-7170   _pause_resume_cmd
  2031-2075   _persist_refreshed_cookies
  1934-1966   _pick_checked_pull_proxy
  9840-9853   _pin_auth_value
  9899-9900   _pin_clear_fail
  9879-9882   _pin_locked
  9885-9896   _pin_note_fail
  9856-9876   _pin_ok
 19889-19914  _piper_pick_model
 19974-20025  _piper_say
 12331-12366  _post_json_threaded
 13408-13426  _probe_video_size
  1817-1834   _proc_is_recorder
 10755-10783  _proxy_pool_refresh_loop
  1900-1931   _proxy_report_recording
  8515-8553   _pruefstand_melden
 24033-24044  _pruefung_verworfen
 11981-11983  _prune_stall_dumps
 11132-11302  _public_stats
  2097-2103   _pull_proxy_still
 17494-17520  _push_notify
 10059-10061  _pwa_dir
 10512-10527  _quick_validate_proxy
 12397-12399  _quiet_hours_config
 10024-10057  _rate_guard
 16762-16768  _react_warn
  7622-7661   _reap_proc
  9051-9118   _rec_auto_abschalten
  8998-9048   _rec_frueh_getrennt
  8881-8943   _rec_kategorie_melden
  8946-8995   _rec_totstreak_fortschreiben
  2544-2566   _record_check_outcome
   794-796    _redact_stream_urls
 10682-10752  _refresh_proxy_pool
  2321-2412   _resolve_via_html
  2694-2891   _resolve_via_webcast_api_v2
  2954-3039   _resolve_via_ytdlp
 22084-22213  _resolve_youtube_ingest
  2298-2318   _resolver_stumm
 12820-12831  _restream_active_sources
 13757-13881  _restream_avatar_feeder_start
 13884-13893  _restream_avatar_feeder_stop
 18135-18253  _restream_chat_guardian
 12994-13066  _restream_chat_push
 13091-13100  _restream_chat_push_async
 13509-13618  _restream_html_overlay_start
 13621-13634  _restream_html_overlay_stop
 12779-12802  _restream_overlay_files
 18748-18780  _restream_platform_state
 18948-18983  _restream_resume_after_restart
 13941-14013  _restream_tts_enqueue_wav
 13370-13402  _restream_tts_feeder
 13367-13368  _restream_tts_fifo_path
 13896-13923  _restream_tts_start
 13925-13939  _restream_tts_stop
 18786-18945  _restream_verify_loop
 21118-21130  _retention_loop
 21112-21115  _retention_scan
  2651-2653   _room_is_abo
  5956-6073   _run_ai_call
 12124-12137  _run_async_from_flask
 20410-20413  _run_priv
 25743-25751  _run_selfcheck_and_exit
 21133-21144  _s3_client
  7963-8014   _safe_send
  4826-4842   _sample_net_throughput
  2596-2626   _schedule_next_check
 21066-21109  _scheduler_loop
  4063-4065   _schema_pk
 12141-12146  _scraper_session
 22782-22821  _screen_full
 11497-11534  _sec_headers
  2277-2279   _select_stream_from_data_section
 25463-25740  _selfcheck
  8829-8863   _send_live_notice
  1387-1391   _should_defer_upload
 21634-21670  _shrink_for_discord
 10064-10076  _sicheres_ziel
 20946-20984  _sicherheits_erinnerung_loop
 24576-24593  _sign_health_check
 24596-24615  _sign_health_loop
  4576-4601   _sitzung_bestimmen
  7731-7742   _spawn
 26168-26198  _spawn_from_flask
 24047-24053  _speicher_maps
 24056-24071  _speicher_pflegen
 17794-18073  _start_chat_listener
 24016-24030  _start_gesperrt
 12104-12121  _start_loop_watchdog
 11329-11378  _stats_loop
 11308-11311  _stats_output_path
 11314-11326  _stats_write
 19926-19940  _stimme_saubern
 19947-19971  _stimme_schon_gesagt
  8496-8512   _storage_cleanup_loop
 24635-24642  _story_for
  3479-3485   _stream_url_expiry
  3487-3492   _stream_url_ttl
 15991-15998  _streamer_persona_get
 21250-21402  _system_backup
 21411-21441  _system_backup_loop
 11941-11959  _task_auf_bot_schleife
 23595-23611  _telegram_befehlsmenue
  7785-7831   _telegram_polling_fehler
 10464-10503  _test_proxy
 11010-11026  _testpush_resolve_live
  7939-7960   _tg_sprache_setzen
  8736-8746   _tg_topics_load_into_mem
  8733-8734   _tg_topics_path
  8748-8755   _tg_topics_save
  9814-9822   _token_ok
  8758-8762   _topic_forget
 12417-12428  _tracking_max_duration
  4356-4370   _tracking_remove_cleanup
  4387-4399   _tracking_resume_cleanup
  1629-1652   _try_attach_file_handler
 19916-19924  _tts_cleanup
 10986-10990  _tunnel_effective
 24388-24408  _tunnel_lage
 24464-24516  _tunnel_wacht_loop
 19412-19465  _twitch_channel_status
 22824-22969  _twitch_chat_loop
 21926-21939  _twitch_clip_versuchen
 22638-22741  _twitch_eventsub_loop
  1410-1423   _upload_queue_add
  1434-1436   _upload_queue_count
  1393-1402   _upload_queue_load
  1383-1385   _upload_queue_path
  1425-1432   _upload_queue_remove
  1404-1408   _upload_queue_save
  1438-1479   _upload_window_loop
  7595-7602   _uptime_s
 12756-12765  _url_host
  3153-3252   _url_nachschlag
   875-879    _usage_record_claude
 24749-24771  _v37_pause_source
 24713-24723  _v37_restream_restart
 24726-24746  _v37_unpause_source
  7862-7906   _verbindung_verloren
  6685-6716   _viewer_sample_loop
  9903-9906   _wants_html
  7605-7619   _warn_empty_env
 24201-24322  _watchdog_loop
 22359-22367  _wchat_thank_ok
 17562-17592  _whisper_get_model
  7692-7699   _whisper_native_section
 16749-16755  _whisper_pool
 17686-17718  _whisper_segments
 17594-17610  _whisper_stumm
 17613-17683  _whisper_transcribe
 13162-13324  _write_restream_overlay
 13124-13159  _write_restream_overlay_async
 22993-23089  _youtube_api_chat_loop
 19468-19571  _youtube_api_status
 19574-19641  _youtube_channel_status
 23092-23253  _youtube_chat_loop
 21942-21967  _youtube_clip_versuchen
 22219-22232  _youtube_restream_autoconfig
 22235-22259  _youtube_restream_autoconfig_inner
 22326-22354  _youtube_send
 19709-19750  _youtube_set_channel
 22262-22296  _yt_access_token
 22299-22314  _yt_live_chat_id
 22322-22323  _yt_sendrate_cfg
 22972-22987  _yt_timeout
  2938-2939   _ytdlp_detect_available
  2941-2952   _ytdlp_note_result
 11986-11988  _zombie_child_count
  7471-7495   about
  4267-4271   add_ai_log_entry
  4184-4187   add_archive_entry
  4864-4866   add_archive_rule
  4604-4675   add_recording
  4331-4348   add_tracking
  6076-6109   ai
  3878-3959   ai_chat
  3993-4003   ai_history_append
  4005-4010   ai_history_clear
  3982-3991   ai_history_load
  3967-3980   ai_rate_limit_check
  6138-6146   aireset
 17091-17110  azrael_chat
 23258-23380  brain_cmd
  3495-3500   build_recording_cmd
  4351-4354   bulk_add_trackings
  6939-6998   bulkadd
  8556-8716   check_all_trackings
  4403-4415   claim_live_transition
 16068-16681  class KickModerator
 14090-15831  class RestreamManager
 10869-10911  classify_proxy_anonymity
  6184-6382   cleanup
  5154-5160   cleanup_old_recordings
  4549-4556   clear_recording
 21970-22041  clip_moment
  4816-4819   compute_storage_forecast
  7061-7134   cookies_cmd
  4322-4328   count_trackings_for_chat
  4254-4265   decide_preferred_recorder
  4194-4197   delete_archive_entry
  4868-4870   delete_archive_rule
  5613-5760   diag
 23492-23553  einnahmen_cmd
  4810-4813   find_recordings_by_fingerprint
  4215-4231   finish_recording_attempt
  4375-4377   get_all_active_trackings
  4282-4284   get_all_checks
  4677-4680   get_all_recordings
  4759-4761   get_all_tags_with_counts
  4787-4790   get_annotations_for_recording
  4189-4192   get_archive_entry
  4780-4783   get_bookmarked_recordings
  2137-2142   get_cookie_health
  4747-4753   get_event_log
  4238-4252   get_last_recording_attempt
  3255-3297   get_live_status
  5093-5096   get_manual_recordings
  4795-4798   get_or_compute_inspect_sync
  5195-5198   get_outcome_breakdown
  4766-4769   get_priority_poll_interval
  4233-4236   get_recent_recording_attempts
  4682-4685   get_recording_by_id
  4773-4776   get_recording_note
  3666-3695   get_redis
  4311-4314   get_stats
  5148-5152   get_storage_stats
  4888-4890   get_tiktok_status_distribution
  4417-4426   get_tracking_state
  4372-4373   get_trackings_for_group
  5109-5112   get_trash_recordings
  9178-9646   handle_recording_finished
 23587-23592  hilfe_cmd
  4078-4139   init_db
  4860-4862   list_archive_rules
  5398-5436   live
  8017-8025   live_check_worker
  3750-3789   llm_chat
  3812-3842   llm_chat_sync
  3797-3809   llm_list_models
  4706-4739   log_event
  1751-1784   log_recording_failure
  7284-7333   logs_cmd
 25175-25453  main
  6112-6135   on_ai_media
  7410-7436   on_ai_reply
  7439-7468   on_azrael_mention
  7500-7530   on_callback
 17116-17221  oracle_handle
  7173-7176   pause_tracking
  5208-5213   profile_keyboard
  5351-5395   quelle
  7235-7281   quota
  8419-8493   reaper_loop
  4884-4886   record_tiktok_status
  6151-6181   recstatus
  3697-3705   redis_get_json
  3708-3714   redis_set_json
 23614-23624  report_cmd
 10914-10916  report_proxy_result
  2415-2457   resolve_tiktok_live_stream
  5104-5107   restore_recording
  7179-7182   resume_tracking
  4873-4878   run_archive_rules
 23627-23884  run_bot
 11838-11932  run_flask
  4848-4851   sample_bandwidth_for_active
  4274-4280   save_tiktok_check
  4541-4547   set_recording_file
  4380-4384   set_tracking_paused
  5099-5102   soft_delete_recording
  8869-8879   split_and_send_video
  5261-5303   start
  4199-4213   start_recording_attempt
  6385-6423   stats
  5038-5091   stop_manual_recording
  7185-7232   stoprec
  6609-6617   summary_cmd
  7336-7407   sysres
  5762-5906   teststream
  5305-5346   tiktok
  7001-7058   topusers
  5473-5530   track
  5438-5470   track_exact
  5544-5611   tracklist
  4922-5036   trigger_manual_recording
  4502-4539   try_acquire_recording_lock
  5115-5117   universal_search
 23556-23584  unpause_cmd
  5532-5542   untrack
 23383-23489  update_cmd
  4805-4808   update_recording_fingerprint
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
betriebslage.py        abschiedswache, bereit, bewerten, haengende_threads, sichern_beim_stopp
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
kickapi.py             app_token, broadcaster_id, channel_info, class PusherGeschlossen, configure, oauth_exchange, pusher_fehler, pusher_lage, pusher_pause, pusher_url, schliessgrund, search_category, send_message, slug, timeout_user, update_channel, user_token
kindprozess.py         alle_beenden, ausfuehren, beenden, lage, zuruecksetzen
kiwahl.py              backend, lokal_stand, lokal_zuerst, normal, provider
lagebild.py            bauen, restream_lage
lastvorsorge.py        freie_kerne, jung, startstufe
laufstand.py           befehl, veraltet, vergleich
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
livecache.py           aufraeumen, aufraeumen_faellig, dauer, einflug, frisch, holen, setzen, statistik, zaehle, zaehler_zuruecksetzen
livefolge.py           beste_url, braucht_url_nachschlag, hat_stream_url, last_dehnung, live_gesehen, offline_bestaetigt, poll_abstand, ruhezeit
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             fuer_log, redact_cookie_zeilen, redact_pull_urls, redact_stream_urls, url_ohne_zugang
logschleuse.py         class Schleuse, einreihen, entkoppeln, nachziehen, schwaerzen, stoppen, synchrone_handler, verloren, wartend, zuruecksetzen
looplag.py             bremser, erfassen, lage, spaeher_starten, stelle_aus_rahmen, takt, zuruecksetzen
loyalty.py             award_chat, award_return, configure, enabled, leaderboard, rank_for, status
mariadbumzug.py        class UmzugAbgebrochen, env_setzen, geoeffnet_von, in_benutzung, quelle_zaehlen, umziehen, vergleichen, ziel_zaehlen
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
profildetail.py        datum, felder, kennzahlen, kontotyp, verlauf
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
prueflage.py           fuer_healthz, lage, merken, uebersicht, vergessen
qrsvg.py               qr_svg
quellprobe.py          empfehlung, form, kurz, main, maske, messen, probe_durchreicher, probe_ffprobe, probe_html, probe_ytdlp, ttl
quellstat.py           lage, zaehlen, zuruecksetzen
reccmd.py              build_recording_cmd, configure
recdb.py               configure, find_recordings_by_fingerprint, get_all_checks, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
resolvergrund.py       http_grund, quelle_lage, quelle_laut, text
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, ein_start_je_ziel, fenstergroesse, freigeben, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, startend, url_host
restreamcfg.py         active_platforms, aktiv, bereite_ziele, bruecke, bruecke_luecke, bruecke_offline, chat_src_ok, discord_invite, enabled, ingest, key_gesetzt, kick_channel_url, overlay, stall_timeout, verify, verify_karenz, verify_misses, verify_takt, yt_oauth_configured, ziel
restreamcmd.py         build, configure, drossel_avatar_aus, drossel_bitrate, drossel_canvas, drossel_fps, drossel_preset, drossel_zusatz, fueller, quell_eingang, schriftart, zubringer
restreamgesundheit.py  blind_markieren, frische_tee_fehler, marke_setzen
restreamstate.py       guard, haken, laufende, layout_mode, mgr
restrend.py            rising_trend
retention.py           scan
revenue.py             is_revenue_platform, normalisieren, sql_in
schema.py              anlegen, create_schema, index_sicher, parameter, spalten_nachziehen
schemastand.py         lege_an, lies, pruefe, schreibe, streng
schnappschuss.py       class Schnappschuss
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendebruecke.py        class Bruecke, class TsUmschreiber, ist_keyframe, pat_pmt_pid, pes_zeit, pid, pmt_stroeme, pmt_urteil, video_pid
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sicherpfad.py          pruefe_unter, sicher_join, sicherer_name, unter
sicherungspruefung.py  archiv_lesbar, dump_vollstaendig, pruefen
speicherpflege.py      abgelaufene_weg, alte_stempel_weg, groessen
sqldialekt.py          bei_konflikt
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
telegramfehler.py      dauer_text, grund, ist_fehler, ist_telegram_chat, text, zuruecksetzen
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tgmarkdown.py          html_zu_md, teilen
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
ytdlpurl.py            nur_frische, urls_aus_json
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
