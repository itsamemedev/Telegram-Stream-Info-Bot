# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
 10069  GET              /                                                dashboard
 12124  GET              /api/abo/status                                  api_abo_status
 12078  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 10857  GET              /api/automation/status                           api_automation_status
 10879  POST             /api/automation/toggle                           api_automation_toggle
 19700  GET              /api/channel/categories                          api_channel_categories
 19706  POST             /api/channel/set                                 api_channel_set
 19553  GET              /api/channels/status                             api_channels_status
 19227  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 19210  GET              /api/clips                                       api_clips
 19256  POST/DELETE      /api/clips/clear                                 api_clips_clear
 19128  GET              /api/debug/threads                               api_debug_threads
 12089  GET              /api/events                                      api_events
 11568  GET              /api/events/stream                               api_events_stream
 11395  GET              /api/health                                      api_health
 19169  POST             /api/highlights/config                           api_highlights_config
 10003  POST             /api/login                                       dashboard_login_submit
 12414  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 11483  GET              /api/notify/status                               api_notify_status
 11494  POST             /api/notify/test                                 api_notify_test
 12178  GET              /api/proxy/heatmap                               api_proxy_heatmap
 12155  GET              /api/proxy/trend                                 api_proxy_trend
 19276  GET              /api/tts/<fn>                                    api_tts_file
 20053  GET              /api/upload_window                               api_upload_window
 11685  GET              /archive/<int:eid>/download                      archive_download
 11713  GET              /download/<int:recording_id>                     download
 11642  GET              /health                                          health
 19040  GET              /healthz                                         healthz
  9994  GET              /login                                           dashboard_login_page
 10024  GET              /logout                                          dashboard_logout
 10031  GET              /manifest.webmanifest                            pwa_manifest
 20026  GET              /overlay                                         overlay_page
 10055  GET              /pwa-icon-<variant>.png                          pwa_icon
 10041  GET              /sw.js                                           pwa_service_worker
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
   322  GET              /api/backoff-watch                               api_backoff_watch   [nc/routes/beobachtung.py]
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
   247  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   529  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   504  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
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
   517  GET              /api/stream/inspect/<username>                   api_stream_inspect   [nc/routes/beobachtung.py]
   376  GET              /api/stream/timeline                             api_stream_timeline   [nc/routes/beobachtung.py]
   406  GET              /api/stream/transcript                           api_stream_transcript   [nc/routes/beobachtung.py]
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
   448  GET              /metrics                                         api_prometheus_metrics   [nc/routes/beobachtung.py]
```

## Discord-Slash-Commands in discordbot.py (65)

```
  2085  /about                  Ueber diesen Bot
   812  /ai                     
  2085  /aireset                KI-Kontext zuruecksetzen
  1216  /ask                    
   913  /assign_role            
   963  /ban                    
  2040  /botstats               
  2085  /brain                  Brain-Lage: Regeln, Agenten, Empfehlungen
  2085  /bulkadd                Mehrere User auf einmal tracken · a b c
  2085  /cleanup                Alte Aufnahmen aufraeumen
  1471  /clearwarns             
  2004  /clip                   
  1989  /clipoftheweek          
  1342  /clips                  
  2085  /cookies                Cookie-Status — mit 'holen' selbst beziehen · [holen]
   868  /create_category        
   839  /create_channel         
   903  /create_group           
   878  /create_role            
   854  /create_voice           
  1099  /daily                  
  2085  /diag                   Vollstaendige Diagnose
  2085  /einnahmen              Einnahmen und Spenden
  1245  /event                  
  1287  /events                 
  1381  /follow                 
  1370  /help                   
   953  /kick                   
  1074  /leaderboard            
  2085  /live                   Live-Status sofort pruefen · @user
  1329  /livenow                
  2085  /logs                   Letzte Fehler aus dem Log
  2085  /pause                  Tracking pausieren · @user
  1357  /post_test              
  1177  /profile                
   985  /purge                  
  2085  /quota                  Speicher-Quota
  1061  /rank                   
  1317  /recstatus              
   923  /remove_role            
  2085  /report                 Azrael-Sentinel-Wochenreport
   825  /restream_status        
  2085  /resume                 Tracking fortsetzen · @user
   933  /set_channel_perms      
  1028  /setup_community        
  1045  /setup_targets          
  1413  /stats                  
   784  /status                 
  2085  /stoprec                Laufende Aufnahme sauber beenden · @user
  1509  /streaminfo             
  2085  /summary                Tageszusammenfassung
  2085  /sysres                 System-Ressourcen
  2085  /teststream             Recorder-Selbsttest · @user
  2085  /tiktok                 Profil-Analyse eines TikTok-Accounts · ‹name›
   973  /timeout                
  1481  /topstreamers           
  2085  /topusers               Top-Streamer nach Aufnahmen
   714  /track                  
  2085  /track_exact            Exakten Usernamen tracken (ohne Korrektur) · ‹name›
   797  /tracklist              
  1395  /unfollow               
  2085  /unpause                Auto-pausierte Quelle wieder aktivieren · @user
   746  /untrack                
  1434  /warn                   
  1457  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2243  on_member_join
  2205  on_message
  2106  on_raw_reaction_add
  2278  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    58-73     konfiguriere
    76-476    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (46 Funktionen)

```
  1586-1637   _award_xp
  1808-1837   _clip_week_leader
  1861-1875   _clipoftheweek_loop
  2394-2456   _community_events_loop
  1543-1565   _dc_client
  1568-1577   _dc_offen
  2496-2531   _disc_automod_check
   402-407    _disc_sprache_setzen
  1640-1688   _discord_ai_automod
   535-574    _discord_automod
  1691-1711   _discord_azrael_reply
  1878-2353   _discord_run_once
   237-295    _discord_start
   298-352    _ensure_discord_invite
  2359-2391   _ensure_error_channel
   423-436    _ensure_rank_roles
   677-691    _ensure_team_roles
  2459-2489   _error_channel_loop
   584-588    _guard
   504-532    _handle_voice_ai
   410-420    _is_admin
  1756-1767   _liveboard_loop
   591-609    _on_level_up
   500-501    _par_chat_id
  1840-1858   _post_clip_of_week
  1770-1788   _post_weekly_digest
   439-465    _provision_base_channels
   468-484    _provision_user_channels
  1309-1402   _reg_betrieb
   999-1088   _reg_community_setup
  1091-1166   _reg_daily_profil
  1209-1306   _reg_frage_events
   771-827    _reg_info
   945-996    _reg_moderation
  1169-1206   _reg_profil
   894-942    _reg_rollen
   830-891    _reg_server
  1405-1492   _reg_streamer
  1495-1540   _reg_system
   705-768    _reg_tracking
   644-674    _run_tg_handler
   487-497    _tracked_usernames
   154-216    _uebernehmen
  1720-1753   _update_liveboard
  1791-1805   _weekly_digest_loop
   219-222    starte
```

## Top-Level-Symbole in bot.py (536 Funktionen, 2 Klassen)

```
 24841-24863  _abbruch_datenbank_unlesbar
  2645-2646   _abo_key
  2666-2684   _abo_probe_dump
 24959-24975  _abschied_wachen
 24978-24996  _abschluss
 15932-15939  _ad_allowlist
 16928-16934  _agent_for
 16937-16953  _ai_telemetry
 17450-17468  _alert
 20921-20971  _alert_monitor_loop
 21335-21397  _announce_loop
  3531-3541   _anthropic_key
  3548-3550   _anthropic_model
  9686-9689   _arg_int
  2637-2642   _as_dict
 24591-24600  _async_exc_handler
 17631-17653  _audio_tap_cmd
 18211-18270  _audio_tap_melden
 17667-17691  _audio_tap_sammler
  9035-9068   _aufnahme_beim_stopp_sichern
 23883-23885  _aufnahme_deckel
  9071-9089   _aufnahme_platz_frei
 24923-24943  _aufnahmen_abschliessen
 24866-24920  _aufraeumen
  9857-9926   _auth_cookie
  9824-9853   _auth_guard
  1887-1892   _auto_on
 18897-18915  _auto_restream_loop
 13626-13668  _avatar_frames_laden
 22418-22433  _azrael_broadcast_reply
 22318-22340  _azrael_chat_reply
 22290-22315  _azrael_chat_should_reply
 22346-22348  _azrael_gate_cfg
 16958-16972  _azrael_live_state
 19939-19953  _azrael_overlay_state
 17332-17386  _azrael_proactive_loop
 16776-16832  _azrael_reaction_to_chats
 22351-22358  _azrael_reply_all_chats
 22277-22287  _azrael_self_names
 22386-22415  _azrael_send_to
 13587-13623  _azrael_spricht
 13930-13943  _azrael_stimme_stumm
 16978-16999  _azrael_system
 21055-21058  _backup_active
 21136-21149  _backup_loop
 23972-23976  _betrieb
 24664-24673  _brain_crowdsec_snap
 20842-20851  _brain_growth_loop
 10248-10275  _brain_growth_snapshot
  2570-2590   _brain_hint_delay
 24736-24771  _brain_moderation_snap
  6433-6461   _brain_notify
 24774-24796  _brain_recording_snap
 24676-24733  _brain_restream_health
 24799-24812  _brain_tiktok_status_snap
 11547-11564  _browser_push
  6473-6560   _build_daily_summary
 13977-13981  _build_restream_cmd
  5255-5282   _can_stop_tracking
  2000-2022   _capture_set_cookies
 12232-12235  _cfg_get
 12238-12240  _cfg_set
 19661-19696  _channel_set_all
 12815-12818  _chat_connected
 12821-12837  _chat_disconnected
  8678-8689   _chat_is_forum
 18018-18043  _chat_listener_abbauen
 12857-12859  _chat_sanitize
 12800-12812  _chat_stat
 12840-12843  _chat_stats_snapshot
  3849-3861   _check_ai_models_sync
 10530-10573  _classify_pool_anonymity
 10576-10593  _classify_pool_anonymity_bg
   879-901    _claude_chat_sync_metered
  9718-9725   _client_ip
 21481-21508  _clip_prune
 21511-21521  _clip_recfile_for
 21934-21940  _clip_should_velocity
 21563-21645  _clip_to_discord
  3735-3744   _close_ai_session
 22464-22479  _cohost_broadcast
 22449-22450  _cohost_cfg
 22505-22517  _cohost_fire_highlight
 22453-22461  _cohost_gate
 22482-22502  _cohost_highlight
 10178-10180  _conv_messages
  6832-6893   _cookie_alarm_loop
  2090-2091   _cookie_autofetch_info
  2074-2078   _cookie_autorefresh_info
 24301-24323  _cookie_bezug_loop
 24326-24351  _cookie_bezug_runde
  1977-1981   _cookie_header
  2103-2117   _cookies_selbst_holen
  4085-4097   _create_index_safe
 20385-20499  _crowdsec_status
 20331-20382  _crowdsec_via_lapi
 20235-20253  _cscli_bin
 20262-20275  _cscli_path
  6722-6747   _daily_summary_loop
 20293-20310  _darf_journal_lesen
  3060-3085   _darf_ytdlp_nachschlagen
 11728-11749  _dashboard_adresse
 20895-20918  _db_maintenance_loop
  6691-6719   _db_vacuum_loop
 15955-15979  _detect_foreign_ad
  1568-1579   _diag_path_owner
 17237-17282  _director_finalize
 18200-18207  _director_for
 17186-17234  _director_mark
 21797-21800  _disc_state_get
 21803-21810  _disc_state_set
 20823-20832  _discord_bot_starten
 20786-20797  _discord_einladung_merken
 20835-20839  _discord_invite
 20800-20820  _discord_kontext
 21758-21794  _discord_live_thread
 17389-17401  _discord_notify
 20758-20783  _discord_ops_alert
 21656-21754  _discord_post_user
 21400-21406  _discord_stop
  6750-6827   _disk_alarm_loop
 24226-24275  _disk_autoclean
 24446-24459  _disk_guard_loop
 13565-13572  _drossel_hoeher
 13561-13562  _drossel_stufe
 13575-13583  _drossel_zuruecksetzen
 11905-11907  _dump_all_threads
 10456-10519  _enrich_proxies_with_geo
  2146-2207   _ensure_cookie_file_netscape
  8737-8740   _ensure_notify_topic
 10700-10737  _ensure_proxy_ready
  8691-8718   _ensure_topic
   726-728    _env_int
   731-733    _env_int_range
 17434-17447  _event_webhook
 12583-12596  _evolution_loop
  5875-5909   _extract_file_payload
  2279-2281   _extract_urls_from_streamurl_node
 20278-20285  _f2b_sudo_hint
 24999-25062  _fatal_vom_botteil
 23888-23903  _fd_grenze_anheben
  4719-4729   _fehler_text
 10357-10375  _fetch_proxy_list
 17987-18015  _fetch_tiktok_room_id
   809-812    _ff_cmd
 13394-13399  _find_chromium
  3451-3453   _find_external_recorder
  2284-2286   _find_stream_urls
 12283-12308  _fire_webhooks
  7659-7668   _fork_safe
   912-925    _freeai_chat_sync_metered
 20324-20328  _geo_lookup_ips
  3723-3732   _get_ai_session
  7492-7532   _get_live_info
  2911-2918   _get_resolve_semaphore
  7984-8374   _handle_single_tracking
 24048-24050  _hb
 24053-24070  _hb_while
 12871-12873  _highlight_cfg
 12876-12905  _highlight_observe
 13402-13420  _htmlov_screenshot_cmd
 17693-17703  _httpx_proxy
 12316-12328  _in_quiet_hours
 24827-24838  _init_db_oder_abbruch
 25645-25676  _install_fast_eventloop
  9581-9635   _install_fast_json
 11910-11926  _install_faulthandler
 18943-18952  _intel_ensure_schema
 18995-19030  _intel_index_loop
 18964-18979  _intel_index_one
 18955-18961  _intel_semantic
  5244-5253   _is_authorized
  7870-7891   _is_dead
  2269-2271   _is_hevc
 20313-20315  _is_private_ip
  1786-1793   _is_process_running
  6463-6470   _is_quiet_hours
  1361-1370   _is_upload_window
  4584-4599   _iso
  9670-9683   _json_error_handler
  6685-6686   _kick_broadcaster_id
  6597-6639   _kick_follower_count
  6581-6584   _kick_slug
 11360-11367  _kick_user_token
  7791-7816   _kick_ws_pause
 24815-24824  _kickmod_boot
  4174-4177   _kind_from_filename
 12345-12347  _latest_popularity
  1723-1732   _laufstand
 24409-24443  _laufstand_loop
 23979-24010  _leistung_erheben
 18606-18655  _live_react_loop
 18273-18595  _live_react_worker
  3301-3413   _live_status_aufloesen
 16835-16846  _live_transcript_push
 18597-18604  _live_users
 17285-17329  _living_title_loop
 21061-21133  _local_backup_scan
  9652-9666   _log_5xx
 24013-24045  _log_schleuse_pruefen
   799-806    _log_sicher
 13989-14001  _looks_like_codec_err
 13984-13986  _looks_like_source_expired
  7709-7739   _loop_fehler
 11930-11939  _loop_heartbeat
 23794-23827  _loop_lag_monitor
 23841-23861  _loop_stockung_melden
 23864-23874  _loop_takt_starten
 11942-12015  _loop_watchdog_thread
 16715-16729  _loyalty_add
 16706-16712  _loyalty_get
 16732-16740  _loyalty_top
 12455-12457  _manual_donations_total
  4926-4945   _manual_status
  7893-7894   _mark_dead
 10976-10992  _marketing_loop
 22365-22383  _maybe_handle_command
 24545-24569  _maybe_hype_clip
 21450-21478  _meme_klassifizieren
  4052-4075   _migrate_columns
 22644-22655  _mod_is_exempt
 22658-22663  _mod_warn_first
 22666-22669  _mod_warn_text
 12640-12659  _modlog
 12623-12637  _modlog_schreiben
  1057-1059   _multistream_targets
  3088-3124   _nachschlag_ytdlp
  7671-7672   _nc_create_subprocess_exec
  7675-7676   _nc_create_subprocess_shell
 11297-11314  _news_loop
 12682-12684  _normalize_ingest
  2501-2518   _note_check_duration
  8731-8734   _notify_topic_name
  3127-3147   _ohne_url_melden
 16861-16869  _oracle_memories
 17135-17169  _oracle_memorize
 16872-16885  _oracle_persona
 16854-16858  _oracle_recent_text
 13028-13029  _ov_atomic_write
 13019-13021  _ov_bar
 15858-15870  _ov_clip_text
 13024-13025  _ov_oneline
 19990-20019  _overlay_push
 13348-13391  _overlay_render_size
 12751-12755  _overlay_session_reset
 19955-19957  _overlay_src_ok
 15942-15952  _own_invites
 13343-13345  _parse_size
 20507-20587  _parse_ssh_attacks
  7094-7127   _pause_resume_cmd
  2028-2072   _persist_refreshed_cookies
  1931-1963   _pick_checked_pull_proxy
  9754-9767   _pin_auth_value
  9813-9814   _pin_clear_fail
  9793-9796   _pin_locked
  9799-9810   _pin_note_fail
  9770-9790   _pin_ok
 19797-19822  _piper_pick_model
 19882-19933  _piper_say
 12245-12280  _post_json_threaded
 13322-13340  _probe_video_size
  1814-1831   _proc_is_recorder
 10669-10697  _proxy_pool_refresh_loop
  1897-1928   _proxy_report_recording
 23923-23934  _pruefung_verworfen
 11895-11897  _prune_stall_dumps
 11046-11216  _public_stats
  2094-2100   _pull_proxy_still
 17405-17431  _push_notify
  9973-9975   _pwa_dir
 10426-10441  _quick_validate_proxy
 12311-12313  _quiet_hours_config
  9938-9971   _rate_guard
 16676-16682  _react_warn
  7579-7618   _reap_proc
  8965-9032   _rec_auto_abschalten
  8912-8962   _rec_frueh_getrennt
  8795-8857   _rec_kategorie_melden
  8860-8909   _rec_totstreak_fortschreiben
  2541-2563   _record_check_outcome
   794-796    _redact_stream_urls
 10596-10666  _refresh_proxy_pool
  2318-2409   _resolve_via_html
  2691-2888   _resolve_via_webcast_api_v2
  2951-3036   _resolve_via_ytdlp
 21974-22103  _resolve_youtube_ingest
  2295-2315   _resolver_stumm
 12734-12745  _restream_active_sources
 13671-13795  _restream_avatar_feeder_start
 13798-13807  _restream_avatar_feeder_stop
 18046-18164  _restream_chat_guardian
 12908-12980  _restream_chat_push
 13005-13014  _restream_chat_push_async
 13423-13532  _restream_html_overlay_start
 13535-13548  _restream_html_overlay_stop
 12693-12716  _restream_overlay_files
 18659-18691  _restream_platform_state
 18859-18894  _restream_resume_after_restart
 13855-13927  _restream_tts_enqueue_wav
 13284-13316  _restream_tts_feeder
 13281-13282  _restream_tts_fifo_path
 13810-13837  _restream_tts_start
 13839-13853  _restream_tts_stop
 18697-18856  _restream_verify_loop
 21026-21038  _retention_loop
 21020-21023  _retention_scan
  2648-2650   _room_is_abo
  5913-6030   _run_ai_call
 12038-12051  _run_async_from_flask
 20318-20321  _run_priv
 25633-25641  _run_selfcheck_and_exit
 21041-21052  _s3_client
  7920-7971   _safe_send
  4852-4868   _sample_net_throughput
  2593-2623   _schedule_next_check
 20974-21017  _scheduler_loop
  4078-4082   _schema_pk
 12055-12060  _scraper_session
 22672-22711  _screen_full
 11411-11448  _sec_headers
  2274-2276   _select_stream_from_data_section
 25353-25630  _selfcheck
  8743-8777   _send_live_notice
  1384-1388   _should_defer_upload
 21524-21560  _shrink_for_discord
  9978-9990   _sicheres_ziel
 20854-20892  _sicherheits_erinnerung_loop
 24466-24483  _sign_health_check
 24486-24505  _sign_health_loop
  4602-4627   _sitzung_bestimmen
  7688-7699   _spawn
 26058-26088  _spawn_from_flask
 23937-23943  _speicher_maps
 23946-23961  _speicher_pflegen
 17705-17984  _start_chat_listener
 23906-23920  _start_gesperrt
 12018-12035  _start_loop_watchdog
 11243-11292  _stats_loop
 11222-11225  _stats_output_path
 11228-11240  _stats_write
 19834-19848  _stimme_saubern
 19855-19879  _stimme_schon_gesagt
  8453-8469   _storage_cleanup_loop
 24525-24532  _story_for
  3476-3482   _stream_url_expiry
  3484-3489   _stream_url_ttl
 15905-15912  _streamer_persona_get
 21158-21292  _system_backup
 21301-21331  _system_backup_loop
 11855-11873  _task_auf_bot_schleife
 23485-23501  _telegram_befehlsmenue
  7742-7788   _telegram_polling_fehler
 10378-10417  _test_proxy
 10924-10940  _testpush_resolve_live
  7896-7917   _tg_sprache_setzen
  8650-8660   _tg_topics_load_into_mem
  8647-8648   _tg_topics_path
  8662-8669   _tg_topics_save
  9728-9736   _token_ok
  8672-8676   _topic_forget
 12331-12342  _tracking_max_duration
  4382-4396   _tracking_remove_cleanup
  4413-4425   _tracking_resume_cleanup
  1626-1649   _try_attach_file_handler
 19824-19832  _tts_cleanup
 10900-10904  _tunnel_effective
 24278-24298  _tunnel_lage
 24354-24406  _tunnel_wacht_loop
 19320-19373  _twitch_channel_status
 22714-22859  _twitch_chat_loop
 21816-21829  _twitch_clip_versuchen
 22528-22631  _twitch_eventsub_loop
  1407-1420   _upload_queue_add
  1431-1433   _upload_queue_count
  1390-1399   _upload_queue_load
  1380-1382   _upload_queue_path
  1422-1429   _upload_queue_remove
  1401-1405   _upload_queue_save
  1435-1476   _upload_window_loop
  7552-7559   _uptime_s
 12670-12679  _url_host
  3150-3249   _url_nachschlag
   872-876    _usage_record_claude
 24639-24661  _v37_pause_source
 24603-24613  _v37_restream_restart
 24616-24636  _v37_unpause_source
  7819-7863   _verbindung_verloren
  6642-6673   _viewer_sample_loop
  9817-9820   _wants_html
  7562-7576   _warn_empty_env
 24091-24212  _watchdog_loop
 22249-22257  _wchat_thank_ok
 17473-17503  _whisper_get_model
  7649-7656   _whisper_native_section
 16663-16669  _whisper_pool
 17597-17629  _whisper_segments
 17505-17521  _whisper_stumm
 17524-17594  _whisper_transcribe
 13076-13238  _write_restream_overlay
 13038-13073  _write_restream_overlay_async
 22883-22979  _youtube_api_chat_loop
 19376-19479  _youtube_api_status
 19482-19549  _youtube_channel_status
 22982-23143  _youtube_chat_loop
 21832-21857  _youtube_clip_versuchen
 22109-22122  _youtube_restream_autoconfig
 22125-22149  _youtube_restream_autoconfig_inner
 22216-22244  _youtube_send
 19617-19658  _youtube_set_channel
 22152-22186  _yt_access_token
 22189-22204  _yt_live_chat_id
 22212-22213  _yt_sendrate_cfg
 22862-22877  _yt_timeout
  2935-2936   _ytdlp_detect_available
  2938-2949   _ytdlp_note_result
 11900-11902  _zombie_child_count
  7428-7452   about
  4293-4297   add_ai_log_entry
  4210-4213   add_archive_entry
  4890-4892   add_archive_rule
  4630-4701   add_recording
  4357-4374   add_tracking
  6033-6066   ai
  3875-3956   ai_chat
  3990-4000   ai_history_append
  4002-4007   ai_history_clear
  3979-3988   ai_history_load
  3964-3977   ai_rate_limit_check
  6095-6103   aireset
 17002-17021  azrael_chat
 23148-23270  brain_cmd
  3492-3497   build_recording_cmd
  4377-4380   bulk_add_trackings
  6896-6955   bulkadd
  8472-8630   check_all_trackings
  4429-4441   claim_live_transition
 15982-16595  class KickModerator
 14004-15745  class RestreamManager
 10783-10825  classify_proxy_anonymity
  6141-6339   cleanup
  5180-5186   cleanup_old_recordings
  4575-4582   clear_recording
 21860-21931  clip_moment
  4842-4845   compute_storage_forecast
  7018-7091   cookies_cmd
  4348-4354   count_trackings_for_chat
  4280-4291   decide_preferred_recorder
  4220-4223   delete_archive_entry
  4894-4896   delete_archive_rule
  5570-5717   diag
 23382-23443  einnahmen_cmd
  4836-4839   find_recordings_by_fingerprint
  4241-4257   finish_recording_attempt
  4401-4403   get_all_active_trackings
  4308-4310   get_all_checks
  4703-4706   get_all_recordings
  4785-4787   get_all_tags_with_counts
  4813-4816   get_annotations_for_recording
  4215-4218   get_archive_entry
  4806-4809   get_bookmarked_recordings
  2134-2139   get_cookie_health
  4773-4779   get_event_log
  4264-4278   get_last_recording_attempt
  3252-3294   get_live_status
  5119-5122   get_manual_recordings
  4821-4824   get_or_compute_inspect_sync
  5221-5224   get_outcome_breakdown
  4792-4795   get_priority_poll_interval
  4259-4262   get_recent_recording_attempts
  4708-4711   get_recording_by_id
  4799-4802   get_recording_note
  3663-3692   get_redis
  4337-4340   get_stats
  5174-5178   get_storage_stats
  4914-4916   get_tiktok_status_distribution
  4443-4452   get_tracking_state
  4398-4399   get_trackings_for_group
  5135-5138   get_trash_recordings
  9092-9560   handle_recording_finished
 23477-23482  hilfe_cmd
  4105-4165   init_db
  4886-4888   list_archive_rules
  5374-5412   live
  7974-7982   live_check_worker
  3747-3786   llm_chat
  3809-3839   llm_chat_sync
  3794-3806   llm_list_models
  4732-4765   log_event
  1748-1781   log_recording_failure
  7241-7290   logs_cmd
 25065-25343  main
  6069-6092   on_ai_media
  7367-7393   on_ai_reply
  7396-7425   on_azrael_mention
  7457-7487   on_callback
 17027-17132  oracle_handle
  7130-7133   pause_tracking
  5234-5239   profile_keyboard
  7192-7238   quota
  8376-8450   reaper_loop
  4910-4912   record_tiktok_status
  6108-6138   recstatus
  3694-3702   redis_get_json
  3705-3711   redis_set_json
 23504-23514  report_cmd
 10828-10830  report_proxy_result
  2412-2454   resolve_tiktok_live_stream
  5130-5133   restore_recording
  7136-7139   resume_tracking
  4899-4904   run_archive_rules
 23517-23774  run_bot
 11752-11846  run_flask
  4874-4877   sample_bandwidth_for_active
  4300-4306   save_tiktok_check
  4567-4573   set_recording_file
  4406-4410   set_tracking_paused
  5125-5128   soft_delete_recording
  8783-8793   split_and_send_video
  5287-5329   start
  4225-4239   start_recording_attempt
  6342-6380   stats
  5064-5117   stop_manual_recording
  7142-7189   stoprec
  6566-6574   summary_cmd
  7293-7364   sysres
  5719-5863   teststream
  5331-5372   tiktok
  6958-7015   topusers
  5449-5506   track
  5414-5446   track_exact
  5520-5568   tracklist
  4948-5062   trigger_manual_recording
  4528-4565   try_acquire_recording_lock
  5141-5143   universal_search
 23446-23474  unpause_cmd
  5508-5518   untrack
 23273-23379  update_cmd
  4831-4834   update_recording_fingerprint
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
prueflage.py           lage, merken, vergessen
qrsvg.py               qr_svg
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
